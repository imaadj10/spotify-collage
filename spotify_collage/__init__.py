import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4d206d80d5354c7ca49248eb616d2db9",
                                               client_secret="29456c8c9b994ccc958a2ac4594857d3",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-library-read"))

