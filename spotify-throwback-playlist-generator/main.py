from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

date = input('Enter a date to grab a Hot 100 playlist (YYYY-MM-DD): ')
year = date.split("-")[0]

# scrape billboard hot 100
URL = "https://www.billboard.com/charts/hot-100/"
response = requests.get(f"{URL}{date}").text
soup = BeautifulSoup(response, 'html.parser')

# pick out songs
all_song_elements = soup.main.find_all(name="h3", id="title-of-a-story", class_="u-max-width-230@tablet-only")
all_artists = soup.find_all(name="span", class_="u-max-width-230@tablet-only")

# clean up lists
songs = [item.getText().replace("\t","").replace("\n","") for item in all_song_elements]
artists = [artist.getText().replace("\t","").replace("\n","") for artist in all_artists]

# spotify api
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://example.com/',
        cache_path='token.txt',
        show_dialog=True
    )
)
user_id = sp.current_user()['id']

# search for songs
playlist_songs = []
for i in range(len(songs)):
    track = sp.search(q=f"track:{songs[i]}, year:{year}", type="track")
    try:
        playlist_songs.append(track['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{songs[i]} by {artists[i]} not found in Spotify. Skipped.")


# create playlist
playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard Hot 100", public=False)

# add to playlist
sp.playlist_add_items(playlist_id=playlist['id'],items=playlist_songs)
