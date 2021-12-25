import os
import re
import requests
import spotipy
import pandas as pd
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

pattern = '[0-9]{4}[-][0-9]{2}[-][0-9]{2}'
SPOTIPY_CLIENT_ID = os.getenv("CLIENTID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENTSECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    ))

username = sp.current_user()["id"]


def query_list():
    while True:
        user_input = input("Do you want Billboard or Triple J? ").lower().strip()
        if user_input != "billboard" and user_input != "triple j":
            print("Choose Billboard or Triple J.\n")
            continue
        return user_input


def query_date():
    while True:
        user_input = input("What date do you want to travel to? (Format: YYYY-MM-DD): ")
        if not re.match(pattern, user_input):
            print("Follow the format YYYY-MM-DD, buddy.\n")
            continue
        return user_input


def get_titles(date, source):
    current_year = int(date.split('-')[0])
    if str.lower(source) == "billboard":
        url = f"https://www.billboard.com/charts/hot-100/{date}"
        response = requests.get(url)
        billboard_website = response.text
        soup = BeautifulSoup(billboard_website, "html.parser")
        tracknames = soup.find_all("div", class_="o-chart-results-list-row-container")
        top_titles = [item.find("h3").getText().strip("\n") for item in tracknames]
        return current_year, top_titles

    elif str.lower(source) == "triple j":
        url = f"https://en.wikipedia.org/wiki/Triple_J_Hottest_100,_{current_year}"
        response = requests.get(url)
        website = response.text
        soup = BeautifulSoup(website, "html.parser")
        wikipedia_table = soup.find('table', {'class': "wikitable"})
        as_list = pd.read_html(str(wikipedia_table))
        df = pd.DataFrame(as_list[0]).set_index('#')
        top_titles = df['Song'].tolist()
        return current_year, top_titles

    else:
        return None


def find_uris(tracks, target_year):
    track_uris = []
    year_prev = int(target_year - 1)

    for name in tracks:
        query = f"track: {name}, year: {year_prev}-{target_year}"
        try:
            uri = sp.search(q=query, type="track", limit=1)['tracks']['items'][0]['uri']
        except IndexError:
            # track_uris.append(f'uri for {name} not found')
            pass
        else:
            track_uris.append(uri)
    return track_uris


def clean_up_tracks(uri_list):
    for item in uri_list:
        if 'uri' in item:
            # del uri_list[uri_list.index(item)]
            uri_list.remove(item)
    return uri_list


def create_playlist(track_source, date, tracks):
    if track_source == "triple j":
        playlist_name = f"{track_source.title()} Hottest 100 for {date.split('-')[0]}"
    elif track_source == "billboard":
        playlist_name = f"{track_source.title()} Top Tracks for {date}"
    else:
        playlist_name = "None"
    new_playlist = sp.user_playlist_create(user=username, name=playlist_name, public=False)
    sp.playlist_add_items(playlist_id=new_playlist['id'], items=tracks)
    print(f"\n{track_source} playist for {date} successfully created.")


def main():
    list_type = query_list()
    target_date = query_date()

    year, titles = get_titles(target_date, source=list_type)
    uris = find_uris(titles, year)
    uris_clean = clean_up_tracks(uris)
    create_playlist(list_type, target_date, uris_clean)


if __name__ == "__main__":
    main()
