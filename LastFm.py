import pylast
import time
import SpotifyHandler
import json
import os

# API information for last.fm
API_KEY = os.getenv("LAST_FM_API_KEY")
API_SECRET = os.getenv("LAST_FM_API_SECRET")

# Seconds in a week
WEEK_SECONDS = 604800
cur_time = time.time()

# Authentication for the user
username = os.getenv("USERNAME")
password_hash = pylast.md5(os.getenv("PASSWORD"))
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

# The user library
library = pylast.Library(user=username, network=network)

# List of current albums
cur_album_list = []

# List of albums to remove
albums_to_remove = []

# List of albums to add
albums_to_add = []


# Pushes album data to a text file
def push_to_text():
    json_data = []
    for title in cur_album_list:
        json_data.append(({'title': title}))

    with open('album_data.txt', 'w') as outfile:
        json.dump(json_data, outfile)


# Pulls album data from a text file
def pull_from_text():
    if os.stat("album_data.txt").st_size > 0:
        with open('album_data.txt') as data_file:
            data = json.load(data_file)

        for album_data in data:
            # album = network.get_album(album_data['artist'], album_data['title'])
            cur_album_list.append(album_data['title'])


# Get the albums of the users in the group of the songs listened to in the last week
def get_albums():
    group = network.get_group("Dorm Jam Radio")
    # The group members
    member_array = group.get_members()

    for member in member_array:
        # Gets the albums listened to of each user within a week
        user_songs_to_albums(member)


# Gets the albums listened to of a user
def user_songs_to_albums(user):
    cur_user = network.get_user(user)
    recent_tracks = cur_user.get_recent_tracks(limit=10)

    # Gets the album for each recently played track
    for cur_track in recent_tracks:
        if cur_track.album not in cur_album_list and cur_track.album is not None:
            cur_album_list.append(cur_track.album)
            albums_to_add.append(cur_track.album)
            if len(cur_album_list) >= 10:
                albums_to_remove.append(cur_album_list.pop(0))


# Execute updating loop
pull_from_text()
get_albums()
SpotifyHandler.add_all_albums(albums_to_add)
SpotifyHandler.remove_given_tracks(albums_to_remove)
push_to_text()