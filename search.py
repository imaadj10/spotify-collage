import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import os
os.environ['SPOTIPY_CLIENT_ID'] = '57b136f760bb45edb4540cb94bd6da96'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'b3eab84fe7734966821f9f5d6b16cd64'

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials()
    )

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    print("Input: ")
    name = input()    # let user type input here

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])