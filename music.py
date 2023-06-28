import spotipy
from spotipy.oauth2 import SpotifyOAuth
from random import shuffle


client_id = "d1083a0d79974a4ea073b892268ee9c8"
client_secret = "70fbc8c74bc44a2cb9ef621a29a12e2f"
redirect_uri = "http://localhost:8080"
scope = "user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
playlist_url = "https://open.spotify.com/playlist/4PPFMow4DCYoIFTrOrBEB3"
playlist_id = playlist_url.split('/')[-1]
playlist = sp.playlist(playlist_id, fields="tracks.items.track.id,total")
tracks = playlist['tracks']['items']
track_ids = [track['track']['id'] for track in tracks]

def play():
    songList = [f"spotify:track:{track_id}" for track_id in track_ids]
    shuffle(songList)
    sp.start_playback(uris=songList)
def pause():
    sp.pause_playback()
def resume():
    sp.start_playback()
def Next():
    sp.next_track()
def previous():
    sp.previous_track()

