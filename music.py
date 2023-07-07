import spotipy
from spotipy.oauth2 import SpotifyOAuth
from random import shuffle
from json import load
with open("api_key.json", "r") as f:
    file = load(f)
    client_secret = file["client_secret"]
    client_id = file["client_id"]
try:
    redirect_uri = "http://localhost:8080"
    scope = "user-modify-playback-state user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    playlist_url = "https://open.spotify.com/playlist/4PPFMow4DCYoIFTrOrBEB3"
    playlist_id = playlist_url.split('/')[-1]
    playlist = sp.playlist(playlist_id, fields="tracks.items.track.id,total")
    tracks = playlist['tracks']['items']
    track_ids = [track['track']['id'] for track in tracks]
except Exception as e:
    print("Error" + str(e) + "\n(No internet connection!)")
def play():
    try:
        songList = [f"spotify:track:{track_id}" for track_id in track_ids]
        shuffle(songList)
        sp.start_playback(uris=songList)
    except Exception as e:
        print("No active device found")
def pause():
    sp.pause_playback()
def resume():
    sp.start_playback()
def Next():
    sp.next_track()
def previous():
    sp.previous_track()
def playcustom(playlist_url):
    playlist_id = playlist_url.split('/')[-1]
    playlist = sp.playlist(playlist_id, fields="tracks.items.track.id,total")
    tracks = playlist['tracks']['items']
    track_ids = [track['track']['id'] for track in tracks]
    songList = [f"spotify:track:{track_id}" for track_id in track_ids]
    shuffle(songList)
    sp.start_playback(uris=songList)
def currentSong():
    print("Currently playing:", sp.current_playback()['item']['name'])