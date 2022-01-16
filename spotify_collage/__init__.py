import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="46a88d041bee44a09ec10578836b63bb",
                                               client_secret="a9d14e08e94748d09a38b21421fa590b",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-library-read"))


