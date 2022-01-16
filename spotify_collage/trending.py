from spotify_collage import sp

trending_id = "37i9dQZEVXbMDoHDwVN2tF"

def trending():
    results = sp.playlist_items(trending_id)
    for track in results['items'][:20]:
        print('track    : ' + track['track']['name'])
        print('artist   : ' + track['track']['album']['artists'][0]['name'])
        print('cover art: ' + track['track']['album']['images'][0]['url'])
        print()
