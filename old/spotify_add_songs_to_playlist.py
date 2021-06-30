def get_song_uris_from_playlist(spot, playlist_id):
    songs_info = spot.playlist_tracks(playlist_id=playlist_id)
    uris = []
    for song_info in songs_info['items']:
        uri = song_info['track']['uri']
        uris.append(uri)
    return uris


def add_songs_to_playlist(spot, playlist_id, song_uris):
    print("Getting already included songs")
    included_uris = get_song_uris_from_playlist(spot, playlist_id)
    needed_uris = [uri for uri in song_uris if uri not in included_uris]
    print("Included songs found")
    if len(needed_uris) == 0:
        print("No songs to add")
        return
    print("Adding songs to playlist")
    spot.playlist_add_items(playlist_id, needed_uris)
    print("Added songs to playlist")
    return


if __name__ == '__main__':
    pass
