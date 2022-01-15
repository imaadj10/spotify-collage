from spotify_collage import sp
genres = sp.recommendation_genre_seeds()['genres']

def search_genre():
    genre_name = input("Search for a genre: ")
    if genre_name in genres:
        tracks = sp.recommendations(seed_genres=[genre_name])
        for track in tracks['tracks']:
            print('track    : ' + track['name'])
            print('cover art: ' + track['album']['images'][0]['url'])
            print()
    print(genres)
    
