from spotify_collage.search import search_artist
from spotify_collage.trending import trending

def choose_function(user_choice):
    if user_choice == 1:
        search_artist()
    if user_choice == 2:
        trending()

if __name__ == "__main__":
    user_choice = int(input("Chose a function: "))
    choose_function(user_choice)
