import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="4d206d80d5354c7ca49248eb616d2db9",
                                                           client_secret="29456c8c9b994ccc958a2ac4594857d3"))

def search_artist():
    artist_name = input("Search for an artist: ")
    get_artist_id(artist_name)

def get_artist_id(artist_name):
    url_string = sp.search(q=artist_name, limit=1, offset=0, type='artist', market=None).get('artists').get('items')[0].get('external_urls').get('spotify')
    artist_id = url_string[32:]
    get_top_tracks(artist_id)

def get_top_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id)

    for item in results['tracks'][:16]:
        print('track    : ' + item['name'])
        print('cover art: ' + item['album']['images'][0]['url'])
        print()


if __name__ == "__main__":
    search_artist()




    # lz_uri = 'spotify:artist:757aE44tKEUQEqRuT6GnEB'    roddy ricch
