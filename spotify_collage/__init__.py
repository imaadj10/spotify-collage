import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ee22179f130b461288adca74bed014c6", 
                                                client_secret="6f3daaa8bcf8489a90b11db0cef6e00d",
                                                redirect_uri="http://localhost:8000",
                                                scope="user-library-read"))

