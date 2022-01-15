from spotify_collage.search_artist import search_artist
from spotify_collage.trending import trending
from spotify_collage.search_genre import search_genre

def choose_function(user_choice):
    if user_choice == 1:
        search_artist()
    elif user_choice == 2:
        trending()
    elif user_choice == 3:
        search_genre()

if __name__ == "__main__":
    user_choice = int(input("Chose a function: "))
    choose_function(user_choice)
