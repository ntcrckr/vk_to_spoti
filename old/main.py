from config import *
from emo_parser import parse
from spotify_add_playlist import add_playlist
from spotify_search_song import search_songs
from spotify_add_songs_to_playlist import add_songs_to_playlist

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def log_in_user():
    print("Logging in user.")
    scope = [
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-read-collaborative"
    ]
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=spotify_redirect_uri
        )
    )
    print("Successfully logged in user.")
    return sp


def log_in_bot():
    print("Logging in bot client.")
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret
        )
    )
    print("Successfully logged in bot client.")
    return sp


if __name__ == "__main__":
    url = "https://vk.com/emomew"
    name = "cats and emo"
    playlist_description = f"Playlist made by emo vk fetcher bot. Songs fetched from {url}"

    # get recent songs from <url> as [{'artist': ..., 'song': ...}]
    songs_info = parse(url)
    # ask user to login into spotify
    sp_user = log_in_user()
    # log in bot into spotify
    sp_bot = log_in_bot()
    # if playlist named <name> isn't present, create one
    playlist_id = add_playlist(sp_user, name, playlist_description)
    # find uris of songs from <songs_info>
    uris = search_songs(sp_bot, songs_info)
    # add songs to playlist <name> via their <uris>
    add_songs_to_playlist(sp_user, playlist_id, uris)
