# import os
# from flask import Flask, request, redirect
# from flask_session import Session
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# app = Flask(__name__)
# Session(app)

# @app.route('/')
# def index():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=/.cache)

#     auth_manager = SpotifyOAuth(scope="user-library-read", cache_handler=cache_handler, show_dialog=True))

#     if request.args.get("code"):
#         auth_manager.get_access_token(request.args.get("code"))
#         return redirect('/')

#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         auth_url = auth_manager.get_authorize_url()
#         return f'<h2><a href="{auth_url}">Sign in</a></h2>'

#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return f'<h2>Hi {spotify.me()["display_name"]}, ' \
#            f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
#            f'<a href="/playlists">my playlists</a> | ' \
#            f'<a href="/currently_playing">currently playing</a> | ' \
# 		   f'<a href="/current_user">me</a>' \

# @app.route('/sign_out')
# def sign_out():
#     try:
#         # Remove the CACHE file (.cache-test) so that a new user can authorize.
#         os.remove(session_cache_path())
#         session.clear()
#     except OSError as e:
#         print ("Error: %s - %s." % (e.filename, e.strerror))
#     return redirect('/')

# @app.route('/playlists')
# def playlists():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')

#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user_playlists()


# @app.route('/currently_playing')
# def currently_playing():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     track = spotify.current_user_playing_track()
#     if not track is None:
#         return track
#     return "No track currently playing."


# @app.route('/current_user')
# def current_user():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user()


