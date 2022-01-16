import os
from flask import Flask, session, request, redirect, render_template, url_for
from flask_session import Session
import spotipy
import uuid
from spotify_collage.functions import search_artist, search_genre, saved_songs, trending
from spotify_collage.user import CurrentUser
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return "./.spotify_caches/.cache"

@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-library-read',
                                                cache_handler=cache_handler, 
                                                show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template("index.html")
    # return f'<h2>Hi {spotify.me()["display_name"]}, ' \
    #        f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
    #        f'<a href="/playlists">my playlists</a> | ' \
    #        f'<a href="/currently_playing">currently playing</a> | ' \
	# 	   f'<a href="/current_user">me</a> | ' \
    #        f'<a href = "/artist_top_tracks"> artist_top_tracks</a> | ' \
    #        f'<a href = "/genre_rec"> genre_recommendations</a>' 


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template('playlist.html')


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    track_artist = spotify.artist(track['item']['artists'][0]['id'])
    track_image = track['item']['album']['images'][0]['url']
    track_album = track['item']['album']['name'] 
    track_name = track['item']['name']
    return render_template('current_user.html', title=track_name, artist=track_artist, album=track_album, image=track_image)
    

@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager) #return render_template('current_user.html')
    results = spotify.current_user()
    user = CurrentUser(results['display_name'], results['images'][0]['url'], results['external_urls']['spotify'])
    return render_template('current_user.html', username=user.username, image_url=user.user_image, spotify_link=user.redirect)
    

@app.route('/artist_top_tracks', methods=["GET", "POST"])
def top_artist_tracks():
    top_tracks = []
    images = []
    links = []
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.method == "POST":
        artist_name = request.form["artist_rec"]
        def get_artist_id(artist_name):
            artist_id = (spotify.search(q=artist_name, limit=1, offset=0, type='artist', market=None)['artists']['items'][0]['external_urls']['spotify'][-22:])
            print('\n'+str(artist_name)+"'s artist ID is "+artist_id+'\n')
            results = spotify.artist_top_tracks(artist_id)
            
            for item in results['tracks'][:16]:
                # print('track    : ' + item['name'])
                # print('cover art: ' + item['album']['images'][0]['url']+'\n')
                top_tracks.append(item['name'])
                images.append(item['album']['images'][0]['url'])
        
        get_artist_id(artist_name)
        # return render_template('artistImage&Covers.html', top_tracks=top_tracks , images=images)
        return render_template('artistImage&Covers.html' , top_tracks=top_tracks , images=images, name=artist_name)
        top_tracks = search_artist(spotify)
        print(top_tracks)

    else: 
        return render_template('artist.html', top_tracks = top_tracks)
    #return render_template('artist.html', form=form)
    

@app.route('/genre_rec', methods=["GET", "POST"])
def genre_rec():
    tracklist = []
    imagesGenre = []
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.method == "POST":
        genre_name = request.form["genre_rec"]
        resultsGenre = spotify.recommendations(seed_genres=[genre_name])
        for track in resultsGenre['tracks']:
            print('track    : ' + track['name'])
            print('cover art: ' + track['album']['images'][0]['url'])
            tracklist.append(track['name'])
            imagesGenre.append(track['album']['images'][0]['url'])
            print()
        print(tracklist)
        print(imagesGenre)
        return render_template('genre_rec.html', tracklist=tracklist, images=imagesGenre)

    else:
        return render_template('genre.html', tracklist = tracklist)



@app.route('/trending')
def trending_tracks():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    top_tracks = trending(spotify)
    return render_template('trending.html', top_tracks=top_tracks)

@app.route('/about')
def about():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    return render_template('about.html')
    
@app.route('/your_saved_songs')
def view_saved():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    top_tracks = saved_songs(spotify)
    return render_template('trending.html', top_tracks=top_tracks)


if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("http://127.0.0.1", "5000").split(":")[-1])))