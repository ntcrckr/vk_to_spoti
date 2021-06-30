from debugger import debug

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

import requests
from bs4 import BeautifulSoup

from config import *


class Spoti:
    """Class for everything inside Spotify Web API"""

    def __init__(
            self,
            scope: tuple,
            playlist_name: str,
            playlist_description: str,
            songs_from_vk: dict
    ):
        self.__scope = scope
        self.__sp_user = None
        self.__sp_bot = None
        self.__playlist_name = playlist_name
        self.__playlist_description = playlist_description
        self.__user_id = None
        self.__playlist_id = None
        self.__songs_from_vk = songs_from_vk
        self.__songs_uris_from_search = []
        self.__songs_uris_from_playlist = []
        self.__songs_uris_to_add = []
        debug("Created Spoti object")

    def __del__(self):
        debug("Deleted Spoti object")

    def log_in_user(self):
        debug("Logging in user")
        self.__sp_user = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.__scope,
                client_id=spotify_client_id,
                client_secret=spotify_client_secret,
                redirect_uri=spotify_redirect_uri
            )
        )
        debug("\tSuccessfully logged in user")

    def log_in_bot(self):
        debug("Logging in bot client")
        self.__sp_bot = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=spotify_client_id,
                client_secret=spotify_client_secret
            )
        )
        debug("\tSuccessfully logged in bot client")

    def set_user_id(self):
        debug("Trying to set user id")
        if self.__user_id is None:
            debug("\tTrying to set user id")
            if self.__sp_user is not None:
                debug("\t\tFetched user id")
                self.__user_id = self.__sp_user.me()['id']
            else:
                debug("\t\tCan't fetch user id: user not logged in")
                self.log_in_user()
                self.set_user_id()
        else:
            debug("\tUser id already set")

    def get_playlist_id(self):
        debug(f"Trying to get playlist {self.__playlist_name} id")
        playlists = self.__sp_user.user_playlists(
            user=self.__user_id
        )
        for playlist in playlists['items']:
            if self.__playlist_name == playlist['name']:
                debug(f"\tPlaylist {self.__playlist_name} found")
                self.__playlist_id = playlist['id']
                return
        debug(f"\tPlaylist {self.__playlist_name} not found")

    def create_playlist(self):
        debug("Creating playlist")
        playlist = self.__sp_user.user_playlist_create(
            user=self.__user_id,
            name=self.__playlist_name,
            description=self.__playlist_description
        )
        self.__playlist_id = playlist['id']

    def create_playlist_if_not_found(self):
        debug("Creating playlist if not found")
        self.get_playlist_id()
        if self.__playlist_id is None:
            self.create_playlist()

    def search_for_song(self, artist: str, song: str):
        debug(f"Searching for song {artist} - {song}")
        found = self.__sp_bot.search(
            q=f"{artist} {song}",
            limit=1
        )
        uri = found['tracks']['items'][0]['uri']
        debug(f"\tFound {uri}")
        return uri

    def get_songs_from_info(self):
        debug("Getting songs uris. Searching for songs")
        for song_info in self.__songs_from_vk:
            self.__songs_uris_from_search.append(
                self.search_for_song(song_info['artist'], song_info['song'])
            )
        debug("\tEnded searching for songs")

    def get_songs_uris_from_playlist(self):
        debug("Fetching songs uris from playlist")
        songs_info = self.__sp_user.playlist_tracks(
            playlist_id=self.__playlist_id
        )
        for song_info in songs_info['items']:
            uri = song_info['track']['uri']
            self.__songs_uris_from_playlist.append(uri)
        debug("\tFetched songs uris from playlist")

    def add_songs_to_playlist(self):
        debug("Adding songs to playlist")
        self.__sp_user.playlist_add_items(
            playlist_id=self.__playlist_id,
            items=self.__songs_uris_to_add
        )
        debug("\tAdded songs to playlist")

    def get_songs_uris_to_add(self):
        self.__songs_uris_to_add = [
            uri for uri in self.__songs_uris_from_search
            if uri not in self.__songs_uris_from_playlist
        ]
        debug("\tSongs to add found")

    def add_not_included_songs_to_playlist(self):
        debug("Adding songs to playlist that aren't already included")
        self.get_songs_uris_from_playlist()
        self.get_songs_uris_to_add()
        if len(self.__songs_uris_to_add) == 0:
            print("\tNo songs to add")
            return
        print("\tAdding songs to playlist")
        self.add_songs_to_playlist()
        print("\tAdded songs to playlist")

    def work(self):
        self.log_in_user()
        self.log_in_bot()
        self.set_user_id()
        self.create_playlist_if_not_found()
        self.get_songs_from_info()
        self.get_songs_uris_from_playlist()
        self.add_not_included_songs_to_playlist()


class VK:
    """Class for scraping VK group page"""

    def __init__(
            self,
            vk_group_url: str
    ):
        self.__vk_group_url = vk_group_url
        # noinspection SpellCheckingInspection
        self.__headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/90.0.4430.216 \
                YaBrowser/21.5.4.610 \
                Yowser/2.5 \
                Safari/537.36"
        }
        self.__vk_group_page_text = None
        self.__soup = None
        self.__songs_from_vk_page = []
        debug("Created VK object")

    def __del__(self):
        debug("Deleted VK object")

    def get_page_text(self):
        self.__vk_group_page_text = requests.get(
            url=self.__vk_group_url,
            headers=self.__headers
        ).text

    def get_songs_from_page_text(self):
        self.__soup = BeautifulSoup(
            markup=self.__vk_group_page_text,
            features="html.parser"
        )
        posts = self.__soup.find_all("div", {'class': "wall_text"})
        for post in posts:
            artist = post.find_all("div", {'class': "audio_row__performers"})
            song = post.find_all("span", {'class': ["audio_row__title_inner", "_audio_row__title_inner"]})
            for i in range(len(artist)):
                self.__songs_from_vk_page.append(
                    {
                        'artist': artist[i].find("a").text,
                        'song': song[i].text
                    }
                )

    def get_songs_info(self):
        self.get_page_text()
        self.get_songs_from_page_text()
        return self.__songs_from_vk_page


class VkToSpotify:
    """Parent class for fetching, copying and etc from VK group to Spotify"""

    def __init__(
            self,
            vk_group_url: str,
            playlist_name: str,
            playlist_description: str
    ):
        self.__vk_group_url = vk_group_url
        self.__playlist_name = playlist_name
        self.__playlist_description = playlist_description
        self.__vk = None
        self.__spoti = None
        self.__scope = (
            "playlist-modify-public",
            "playlist-modify-private",
            "playlist-read-private",
            "playlist-read-collaborative"
        )
        debug("Created VkToSpotify object")

    def __del__(self):
        debug("Deleted VkToSpotify object")

    def create_vk(self):
        self.__vk = VK(
            vk_group_url=self.__vk_group_url
        )

    def create_spoti(self, songs_from_vk_page: dict):
        self.__spoti = Spoti(
            scope=self.__scope,
            playlist_name=self.__playlist_name,
            playlist_description=self.__playlist_description,
            songs_from_vk=songs_from_vk_page
        )

    def work(self):
        self.create_vk()
        songs_info = self.__vk.get_songs_info()
        self.create_spoti(songs_info)
        self.__spoti.work()


if __name__ == "__main__":
    url = "https://vk.com/emomew"
    vk_to_spoti = VkToSpotify(
        vk_group_url=url,
        playlist_name="cats and emo",
        playlist_description=f"Playlist made by emo vk fetcher bot. Songs fetched from {url}"
    )
    vk_to_spoti.work()
