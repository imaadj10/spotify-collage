def search_artist():
    artist_name = input("Search for an artist: ")
    get_artist_id(artist_name)

from spotify_collage import sp

def get_artist_id(artist_name):
    url_string = sp.search(q=artist_name, limit=1, offset=0, type='artist', market=None).get('artists').get('items')[0].get('external_urls').get('spotify')
    artist_id = url_string[32:]
    get_top_tracks(artist_id)

def get_top_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id)

    for track in results['tracks']:
        print('track    : ' + track['name'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()