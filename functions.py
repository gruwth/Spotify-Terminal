import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import timedelta as td
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://localhost:8888/callback',
        scope='user-read-playback-state user-read-currently-playing user-modify-playback-state'
    ))
    return sp

def get_current_playing(sp):
    current_track = sp.current_playback()
    if current_track and current_track['item'] is not None:
        track_name = current_track['item']['name']
        artists = ", ".join(artist['name'] for artist in current_track['item']['artists'])
        progress_ms = current_track['progress_ms']
        duration_ms = current_track['item']['duration_ms']
        playing_info = {
            "track_name": track_name,
            "artists": artists,
            "progress_ms": progress_ms,
            "duration_ms": duration_ms,
            "is_playing": current_track["is_playing"],
        }
    else:
        playing_info = {
            "track_name": "No track is currently playing.",
            "artists": "",
            "progress_ms": 0,
            "duration_ms": 0,
            "is_playing": False,
        }
    return playing_info

def toggle_playback(sp, is_playing):
    if is_playing is False:
        sp.start_playback()  # Pause the music
    else:
        sp.pause_playback()  # Play the music

def get_recently_played(sp):
    recent_tracks = sp.current_user_recently_played()
    for track in recent_tracks['items']:
        track_name = track['track']['name']
        artists = ", ".join(artist['name'] for artist in track['track']['artists'])
        album = track['track']['album']['name']
        length = track['track']['duration_ms'] / 1000
        length_str = str(td(seconds=int(length)))[2:]
        print(f"{track_name} | {artists} | {album} | {length_str}")


if __name__ == "__main__":
    sp = authenticate_spotify()
    print(get_recently_played(sp))