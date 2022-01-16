import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import uuid
from spotify_collage.functions import search_artist, search_genre, saved_songs, trending
from spotify_collage.forms import ArtistForm, GenreForm

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
    return spotify.current_user_playlists()


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."

@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()

@app.route('/artist_top_tracks', methods=["GET", "POST"])
def top_artist_tracks():
    form = ArtistForm()
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    if form.validate_on_submit():
        artist = form.artist.data
        top_tracks = search_artist(spotify, artist)
        return render_template('artist.html', top_tracks=top_tracks, form=form)
    return render_template('artist.html', top_tracks = [], form=form)

    
@app.route('/genre_rec', methods=["GET", "POST"])
def genre_rec():
    form = GenreForm()
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    if request.method == "POST":
        top_tracks = search_genre(spotify)
        print(top_tracks)
        return render_template('genre.html', genre=genre, top_tracks=top_tracks, form=form)

    else:
        return render_template('genre.html')

    # if form.validate_on_submit:
    #     genre = form.genre.data
    #     top_tracks = search_genre(spotify)

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