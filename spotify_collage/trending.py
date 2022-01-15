from spotify_collage import sp

def trending():
    # results = sp.search(q='', limit=20)
    # for idx, track in enumerate(results['tracks']['items']):
    #     print(idx, track['name'])
    #print(sp.playlist_cover_image("37i9dQZEVXbMDoHDwVN2tF"))
    results = sp.playlist_items("37i9dQZEVXbMDoHDwVN2tF")

    for item in results['items'][:20]:
        print('track    : ' + item['track']['name'])
        print('cover art: ' + item['album']['images'][0]['url'])
        print()


#"37i9dQZEVXbMDoHDwVN2tF"   # top 50 global