import requests
from bs4 import BeautifulSoup


def get_page_text(url):
    # noinspection SpellCheckingInspection
    my_headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.216 \
            YaBrowser/21.5.4.610 \
            Yowser/2.5 \
            Safari/537.36"
    }
    r = requests.get(url=url, headers=my_headers)
    return r.text


def get_songs_from_page(text_):
    soup = BeautifulSoup(text_, features="html.parser")
    posts = soup.find_all("div", {'class': "wall_text"})
    songs_ = []
    for post in posts:
        artist = post.find("div", {'class': "audio_row__performers"}).find("a").text
        song_ = post.find("span", {'class': ["audio_row__title_inner", "_audio_row__title_inner"]}).text
        songs_.append({'artist': artist, 'song': song_})
    return songs_


def parse(my_url):
    print(f"Getting songs from {my_url}")
    text = get_page_text(my_url)
    print("Songs found:")
    songs = get_songs_from_page(text)
    for song in songs:
        print("\t", song['artist'], " - ", song['song'], sep="")
    return songs


if __name__ == "__main__":
    pass
