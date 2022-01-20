import os
from flask import session, request, redirect, render_template
import spotipy
import uuid
from spotify_collage.functions import search_artist, search_genre, saved_songs, trending
from spotify_collage.user import CurrentUser
from spotify_collage import app

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return "./.spotify_caches/.cache"

@app.route('/')
def index():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-library-read',
                                                cache_handler=cache_handler, 
                                                show_dialog=True, client_id='',
                                                client_secret='',
                                                redirect_uri='')

    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template('sign_in.html', auth_url=auth_url)
        
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template("index.html")


@app.route('/sign_out')
def sign_out():
    try:
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
    trending_id = "37i9dQZEVXbMDoHDwVN2tF"
    results = spotify.playlist_items(trending_id)
    return render_template('test.html')


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if track:
        track_link = track['item']['external_urls']['spotify']
        track_artist = spotify.artist(track['item']['artists'][0]['id'])['name']
        track_image = track['item']['album']['images'][0]['url']
        track_album = track['item']['album']['name'] 
        track_name = track['item']['name']
    else:
        return render_template('currently_play.html', show_button=False)
    return render_template('currently_play.html', title=track_name, artist=track_artist, album=track_album, image=track_image, link=track_link, show_button=True)


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    results = spotify.current_user()
    if len(results['images']) > 0:
        user = CurrentUser(results['display_name'], results['images'][0]['url'], results['external_urls']['spotify'])
    else:
        user = CurrentUser(results['display_name'], "static\images\default_profile.png", results['external_urls']['spotify'])
    return render_template('current_user.html', username=user.username, image_url=user.user_image, spotify_link=user.redirect)


@app.route('/artist_top_tracks', methods=["GET", "POST"])
def top_artist_tracks():
    top_tracks = []
    images = []
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
            
            for item in results['tracks']:
                top_tracks.append(item['name'])
                images.append(item['album']['images'][0]['url'])
        
        get_artist_id(artist_name)
        return render_template('artistImage&Covers.html' , top_tracks=top_tracks , images=images, name=artist_name)
    else: 
        return render_template('artist.html', top_tracks = top_tracks)


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
        return render_template('genre_rec.html', name=genre_name, tracklist=tracklist, images=imagesGenre)
    else:
        return render_template('genre.html', name="", tracklist = tracklist)


@app.route('/trending')
def trending_tracks():
    trending_tracks = []
    trending_artists = []
    trending_images = []
    trending_links = []
    
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    trending_id = "37i9dQZEVXbMDoHDwVN2tF"
    results = spotify.playlist_items(trending_id)
    for track in results['items'][0:]:
        trending_tracks.append(track['track']['name'])
        trending_artists.append(track['track']['album']['artists'][0]['name'])
        trending_images.append(track['track']['album']['images'][0]['url'])
        trending_links.append(track['track']['external_urls']['spotify'])
    return render_template('trending.html', top_tracks=trending_tracks, top_artists=trending_artists, images=trending_images, links=trending_links)


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
    saved_tracks = saved_songs(spotify)['songsNartists']
    saved_pics = saved_songs(spotify)['savedPictures']
    saved_links = saved_songs(spotify)['savedLinks']
    return render_template('liked_songs.html', saved_tracks=saved_tracks, saved_pics=saved_pics , saved_links=saved_links )