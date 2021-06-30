def check_playlist_existing(spot_, uid, name):
    playlists = spot_.user_playlists(uid)
    for playlist in playlists['items']:
        if name == playlist['name']:
            print(f'Playlist {name} found.')
            return playlist['id']
    print(f'Playlist {name} not found. Creating one.')
    return "not found"


def add_playlist(spot, playlist_name, playlist_description):
    print("Adding playlist if needed.")
    user_id = spot.me()['id']
    id_or_nf = check_playlist_existing(spot, user_id, playlist_name)
    if id_or_nf == "not found":
        playlist = spot.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description)
        pid = playlist['id']
        print(f"Playlist's id is {pid}")
        return pid
    print(f"Playlist's id is {id_or_nf}")
    return id_or_nf


if __name__ == '__main__':
    pass
