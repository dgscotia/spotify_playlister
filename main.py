from pprint import pprint

import os
import re
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# TESTING WHETHER IT MERGES ONLINE
# todo clean up the list and remove tracks "not found" --> for some reason not all being removed
# todo figure out why user_playlist_add_tracks not working
# todo rewrite it all into functions

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


def query_date():
    while True:
        user_input = input("What date do you want to travel to? (Format: YYYY-MM-DD): ")
        if not re.match(pattern, user_input):
            print("Follow the format YYYY-MM-DD, buddy.\n")
            continue
        return user_input


def query_username():
    while True:
        user_input = input("What is your Spotify username? ")
        if user_input == "":
            print("Try again, buddy.\n")
            continue
        return user_input


def get_titles(date):
    url = f"https://www.billboard.com/charts/hot-100/{date}"

    current_year = int(date.split('-')[0])

    response = requests.get(url)
    billboard_website = response.text

    soup = BeautifulSoup(billboard_website, "html.parser")

    tracknames = soup.find_all("div", class_="o-chart-results-list-row-container")
    top_100_titles = [item.find("h3").getText().strip("\n") for item in tracknames]
    return current_year, top_100_titles


def find_uris(tracklist, target_year):
    track_uris = []
    year_prev = int(target_year - 1)

    for name in tracklist:
        query = f"track: {name}, year: {year_prev}-{target_year}"
        try:
            uri = sp.search(q=query, type="track", limit=1)['tracks']['items'][0]['uri']
        except IndexError:
            track_uris.append(f'uri for {name} not found')
        else:
            track_uris.append(uri)
    return track_uris


# target_date = query_date()
target_date = "1988-03-08"
# username = query_username()

# list_type = query_list()  # This will be used to choose between Billboard, Pitchfork, Triple-J etc.
list_type = "Billboard"
year, titles = get_titles(target_date)
# uris = find_uris(titles, year)
dummy_uris = ['spotify:track:4cOdK2wGLETKBW3PvgPWqT', 'spotify:track:0L0T4tMAaGqLgIVj1MOj9t', 'spotify:track:7BdXRaSlGAzhySfuW3y8h5', 'spotify:track:5PrhBYkGWarC0svMMuQzlB', 'spotify:track:2iXH35MhsqO5Ry8a7iptpJ', 'spotify:track:5ZY7Gug850kv4heJcWZGHM', 'spotify:track:1kiNatIrwDusOZfR29W0LJ', 'spotify:track:0NzORwlnjFldkBIXEvgqu4', 'spotify:track:0bMG9mHnuAxsb18b2SLAVD', "uri for Can't Stay Away From You not found", 'spotify:track:7cm9QkrwSWH0scegcO8XZ2', 'spotify:track:0pBhA8yQ5FUKyQG13x2Qmh', 'spotify:track:2dykYf0mZG217bYkiREKEh', 'spotify:track:2PFIZFcGry0po3ZfRZkzKc', 'spotify:track:58me6gfG81fNG4v3dpRhh5', 'spotify:track:5n9Ul19Pb8MROfm8eTI7UH', 'spotify:track:0tvKT0EdO4Gm1nw7rgiHHa', 'spotify:track:6SoXgLYqIDiR7Q4Npijwnp', 'spotify:track:01q4ccXbvPlCwZ1fPiFaeM', 'uri for Hungry Eyes (From "Dirty Dancing") not found', 'spotify:track:6LERtd1yiclxFH8MHAqr0Q', 'spotify:track:0sTnQus7pGewDC0UHSyRDS', 'spotify:track:7mJq5UJOfh5yzyjCaiPaZH', 'spotify:track:2PZFLJLct6yrvBcCNEkAw0', 'spotify:track:6fAADiK2jnjdm5QRI7hSYc', 'spotify:track:4b2qn7YRQkVAsbC8pWa7yn', 'spotify:track:2bvzxeD1hPWEYotw40Euq9', 'spotify:track:7tLtIZclwLWk54PFAyDv5T', 'spotify:track:5nW7RbN0mBLPts9CURNwdy', 'spotify:track:7iBav4v8maicL8cWKGxFhQ', 'spotify:track:4741jT3CusJh19viAenNPI', 'spotify:track:73hyTd7EOZHnxDNjCFUVav', "uri for Could've Been not found", 'spotify:track:0O9A61RSHwvVWRnF7wAMAv', "uri for Don't Shed A Tear not found", 'spotify:track:7ujeMX32d72A3mcTytAlbv', 'spotify:track:7DVTNkZRGqvFcKryWCuTZP', 'spotify:track:5QRs63VVKNaqUjg6XSSckM', 'spotify:track:3h04eZTnmFLRMjZajbrp2R', 'spotify:track:6qwTCkJ7red7bQsPxvgHaD', 'spotify:track:4Z7bcUn4gxwPgIItNQv8l1', 'spotify:track:7lJgjvQRJEXcdu19n3Zn5T', 'spotify:track:52LRCeDADRBJmxqoT562yK', 'spotify:track:5aWvinQcbc1W1WdP0GQ6J1', 'spotify:track:3ICZte49haM8ID7H6LSSjb', 'uri for Going Back To Cali (From "Less Than Zero") not found', 'spotify:track:6WoN3Qbw1FfayeJy09rFzR', 'spotify:track:7wBfVgLHlr3GvCO6hqgRyu', 'spotify:track:6WHXaMSnLkooGskzWTT1WN', 'spotify:track:3LFdvM7nIV8t02zyhYLvJo', 'spotify:track:1kGviTmoI8CM1dG0atAek2', 'uri for Hazy Shade Of Winter not found', 'spotify:track:5eLEYt1XuYohJxoZcdXvVw', 'uri for Are You Sure not found', 'spotify:track:1aupoGq6oWjYKOKbabJ0Bm', 'spotify:track:3wyBJokhvt7b1RsPi5GYdW', 'spotify:track:53cZir9KAZSXl2JC3qz2hx', 'uri for Piano In The Dark not found', 'spotify:track:4Y16pBHoeh4IoKpy6INODt', 'spotify:track:254bXAqt3zP6P50BdQvEsq', 'spotify:track:09huOVRryZNV2deKFZLJDC', 'spotify:track:4FGAOmf2vxT7FF8w2vL6R6', 'spotify:track:5G1UUuiREQXwDfpJaxu3BC', 'uri for Kiss And Tell (From "Bright Lights, Big City") not found', 'spotify:track:28fHjGEDS9P4uLah3tN77i', 'spotify:track:1ZomzcopTse4dq2Nfe7Gyd', 'spotify:track:2Cvg3IXEWWMTYTvd8HqpaG', 'spotify:track:1X1TonvQws8wxagWJmnUNj', "uri for Don't Look Any Further not found", "uri for Don't Make A Fool Of Yourself not found", 'uri for Candle In The Wind not found', 'spotify:track:6A48JrV1QyIbmd5cZglvRl', 'spotify:track:29efh6iiRHNXFMJ9FMDqoW', 'spotify:track:6HpPsCidc2enTdicqEmu7t', 'spotify:track:2ZwJYZSzaWc5V5V5V5FUuE', 'spotify:track:14jdxjs33FLmQkNQBDhYV5', 'spotify:track:14mUKa5uIP5wD8SmJbX8ZD', 'uri for Yes (From The Motion Picture "Dirty Dancing") not found', 'uri for Samantha (What You Gonna Do?) not found', 'spotify:track:2oSpQ7QtIKTNFfA08Cy0ku', 'spotify:track:2scXiFuRiqmBZm9pzu8NhF', 'spotify:track:4NsREnHwyAHwxrvVkavclz', 'spotify:track:34sL4eaI8UKWOyYpCvoboU', 'spotify:track:2rUHBIfbMBB92n1gSfSqwF', 'spotify:track:4K3qzy3AR3Lo02ybxs90gW', 'uri for Strange But True\t not found', 'spotify:track:0t1XisESZqQXBaO1yNbRbU', 'spotify:track:0sKlV58cODrjxGFOyf9IXY', 'spotify:track:3lTEXatUG1GWFiDhWsrYAi', 'spotify:track:4IHEOKSPSnPzjKxBktZ4J7', 'spotify:track:202QpSJo7inyEKWeARd5Ax', "uri for She's Only 20 not found", 'spotify:track:3OeUlriM0EZHdWleJtjoVr', 'spotify:track:1FxhasstsR49mNQAfh3qYI', 'uri for Live My Life (From The Film "Hiding Out") not found', 'spotify:track:43oPpqzWPSZmeiwYicmzjG', 'spotify:track:5qMNvVFTJoTLkaXbudbVNF', 'spotify:track:01z7vo9LTHjEoNJydTSJbR', 'spotify:track:5d8byUVc57r4axH3JLbLAX', 'spotify:track:453Y3g7zXpbFhtyzB1agXM']

def clean_up_tracks(dummy_uris):
    for item in dummy_uris:
        if "not found" in item:
            del dummy_uris[dummy_uris.index(item)]
    return dummy_uris


def create_playlist(track_source, date):
    new_playlist = sp.user_playlist_create(user=username, name=f"{track_source} top tracks for {date}", public=False)
    uri = new_playlist['uri']
    pl_id = new_playlist['id']
    return uri, pl_id




def add_tracks():
    pass


playlist_uri = 'spotify:playlist:2RbLeFx52rV9O0Mlv1NyaW'
playlist_id = '2RbLeFx52rV9O0Mlv1NyaW'



# sp.playlist_add_items(playlist_id=playlist_id, items=uris)
