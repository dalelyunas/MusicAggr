__author__ = 'David'

import spotipy
import spotipy.util as util
import os


scope = 'user-library-modify'

#  Client Keys
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = 'http://127.0.0.1:8888/callback'

username = 'musich0lder'

# Gets the authorization token
token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
spotify = spotipy.Spotify(auth=token)


# Removes the given tracks from the spotify playlist
def remove_given_tracks(album_titles):
    for title in album_titles:
        spotify.user_playlist_remove_all_occurrences_of_tracks(username, playlist, get_album_track_uris(title))


# Adds all of the tracks of the stamped album to the spotify playlist
def add_all_albums(album_titles):
    for title in album_titles:
        tracks = get_album_track_uris(title)
        if len(tracks) != 0:
            spotify.user_playlist_add_tracks(username, playlist, tracks)


# Returns the uris of the tracks in the album
def get_album_track_uris(album_title):
    tracks = []
    album = sp.search(album_title, 1, 0, 'album')
    if len(album['albums']['items']) != 0:
        list_of_tracks = sp.album_tracks(album['albums']['items'][0]['uri'])['items']
        for track in list_of_tracks:
            tracks.append(track['uri'])

    print tracks
    return tracks


if token:
    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlists(username)['items'][0]['uri']
    print playlist


else:
    print "Can't get token for", username