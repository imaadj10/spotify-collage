import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="4d206d80d5354c7ca49248eb616d2db9",
                                                           client_secret="29456c8c9b994ccc958a2ac4594857d3"))

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
results = sp.artist_top_tracks(lz_uri)

for item in results['tracks'][:16]:
    print('track    : ' + item['name'])
    print('cover art: ' + item['album']['images'][0]['url'])
    print()
