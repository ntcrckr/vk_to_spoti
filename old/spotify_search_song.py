def search_song(spot, artist: str, song: str):
    print(f"\tSearching for song {artist} - {song}")
    found = spot.search(q=f"{artist} {song}", limit=1)
    uri = found['tracks']['items'][0]['uri']
    print(f"\t\tFound {uri}")
    return uri


def search_songs(spot, songs_info):
    print("Searching for songs")
    song_uris = []
    for song_info in songs_info:
        song_uris.append(search_song(spot, song_info['artist'], song_info['song']))
    print("Ended searching for songs")
    return song_uris


if __name__ == "__main__":
    pass
