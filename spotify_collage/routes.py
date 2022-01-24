import os
from flask import session, request, redirect, render_template
import spotipy
import uuid
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
    return render_template("index.html", name=spotify.current_user()['display_name'])


@app.route('/sign_out')
def sign_out():
    try:
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


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

    track = spotify.current_user_playing_track()
    if track:
        track_artist = spotify.artist(track['item']['artists'][0]['id'])['name']
        track_image = track['item']['album']['images'][0]['url']
        track_album = track['item']['album']['name'] 
        track_name = track['item']['name']
    else:
        return render_template('current_user.html', username=user.username, image_url=user.user_image, spotify_link=user.redirect, show_button=False)

    return render_template('current_user.html', username=user.username, image_url=user.user_image, spotify_link=user.redirect, 
                                                title=track_name, artist=track_artist, album=track_album, image=track_image, show_button=True)


@app.route('/artist_top_tracks', methods=["GET", "POST"])
def top_artist_tracks():
    top_tracks = []
    images = []
    links = []
    names = ["No artist found, please search again"]
    albums = []
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.method == "POST":
        artist_name = request.form["artist_rec"]
        def get_artist_id(artist_name):
            if len(spotify.search(q=artist_name, limit=1, offset=0, type='artist', market=None)['artists']['items']) > 0:
                artist_id = (spotify.search(q=artist_name, limit=1, offset=0, type='artist', market=None)['artists']['items'][0]['external_urls']['spotify'][-22:])
            else:
                return
            results = spotify.artist_top_tracks(artist_id)
            name = spotify.artist(artist_id)['name']
            names[0] = (name)
            for item in results['tracks']:
                top_tracks.append(item['name'])
                images.append(item['album']['images'][0]['url'])
                links.append(item['external_urls']['spotify'])
                albums.append(item['album']['name'])
        
        get_artist_id(artist_name)
        return render_template('artistImage&Covers.html' , top_tracks=top_tracks , images=images, name=names[0], links=links, albums=albums)
    else: 
        return render_template('artist.html')


@app.route('/genre_rec', methods=["GET", "POST"])
def genre_rec():
    tracklist = []
    imagesGenre = []
    links = []
    albums = []
    artists = []
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.method == "POST":
        genre_name = request.form["genre_rec"]
        resultsGenre = spotify.recommendations(seed_genres=[genre_name])
        for track in resultsGenre['tracks']:
            tracklist.append(track['name'])
            imagesGenre.append(track['album']['images'][0]['url'])
            links.append(track['external_urls']['spotify'])
            albums.append(track['album']['name'])
            artists.append(track['album']['artists'][0]['name'])
        return render_template('genre_rec.html', name=genre_name, tracklist=tracklist, images=imagesGenre, links=links, albums=albums, artists=artists)
    else:
        return render_template('genre.html', name="", tracklist = tracklist)


@app.route('/trending')
def trending_tracks():
    trending_tracks = []
    trending_artists = []
    trending_images = []
    trending_links = []
    trending_albums = []
    
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
        trending_albums.append(track['track']['album']['name'])
    return render_template('trending.html', top_tracks=trending_tracks, top_artists=trending_artists, images=trending_images, links=trending_links, top_albums=trending_albums)


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
    
    results = spotify.current_user_saved_tracks(limit=50)
    saved_tracks = []
    saved_artists = []
    saved_pics = []
    saved_links = []
    saved_albums = []

    for idx, item in enumerate(results['items']):
        saved_tracks.append(str(item['track']['name']))
        saved_artists.append(str(item['track']['album']['artists'][0]['name']))
        saved_pics.append(item['track']['album']['images'][0]['url'])
        saved_links.append(item['track']['external_urls']['spotify'])
        saved_albums.append(item['track']['album']['name'])

    return render_template('liked_songs.html', saved_tracks=saved_tracks, saved_pics=saved_pics , saved_links=saved_links, saved_artists=saved_artists, saved_albums=saved_albums)
