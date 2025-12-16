import os
import tqdm
from datetime import datetime
import json
import requests

import src.helper.utils as utils
from src.models.SpotifyAlbum import SpotifyAlbum
from src.models.SpotifyArtist import SpotifyArtist
from src.models.SpotifyPlayer import SpotifyPlayer
from src.models.SpotifyTrack import SpotifyTrack
from src.auth.SpotifyAuth import SpotifyAuth

import pandas as pd

TOKEN_FILE = "/opt/airflow/spotify_project/src/auth/auth_token.json"
DATA_DIR = "/opt/airflow/spotify_project/data"

def get_recently_played(token_info):
  """
  Get user's recently played tracks.

  :param token_info: Dictionary containing access token and its expiration time. 
  :return:
    If success, returns recently played tracks in JSON format.
    If failure, raises an Exception.
  """
  if token_info.get("_access_token") is None: # check if access_token is still valid
    raise Exception("You don't have access, please log in!")

  if datetime.now().timestamp() > token_info.get("_access_token_expiration_time"): # the token is expired
    raise Exception("Session timed out, please refresh the page or log in again.")

  # get user's recently played tracks by including the following header
  headers = {
    "Authorization": f"Bearer {token_info.get('_access_token')}"
  }

  response = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?limit=50", headers=headers) # current user's recently played tracks
  recently_played = response.json()

  return recently_played


def get_artist(artist_id, token_info):
  """
  Get artist information by artist ID.

  :param artist_id: Spotify artist ID.
  :param token_info: Dictionary containing access token and its expiration time.
  :return:
    If success, returns artist information in JSON format.
    If failure, raises an Exception.
  """
  if token_info.get("_access_token") is None: # check if access_token is still valid
    raise Exception("You don't have access, please log in!")

  if datetime.now().timestamp() > token_info.get("_access_token_expiration_time"): # the token is expired
    raise Exception("Session timed out, please refresh the page or log in again.")
  
  headers = {
    "Authorization": f"Bearer {token_info.get('_access_token')}"
  }

  response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers)
  artist_info = response.json()

  return artist_info


def extract_data(recent_played_tracks, token_info):
  
  artist_list = []
  album_list = []
  track_list = []
  playback_list = []

  for item in tqdm.tqdm(recent_played_tracks['items'], desc="Processing tracks", total=len(recent_played_tracks['items'])): # we only focus on the items
    artist_in_a_track_list = []

    track = item['track']
    album, artists = track['album'], track['artists']
    
    # for album
    album_instance = SpotifyAlbum(id=album['id'], name=album['name'], release_date=album['release_date'],
                                  album_type=album['album_type'], total_tracks=album['total_tracks'])
    album_list.append(album_instance)

    # for artists
    for artist in artists:
      artist_info = get_artist(artist['id'], token_info)
      spotify_artist = SpotifyArtist(id=artist_info['id'], name=artist_info['name'], genres=artist_info['genres'])
      artist_in_a_track_list.append(spotify_artist)
    artist_list.extend(artist_in_a_track_list)

    # for tracks
    track_instance = SpotifyTrack(id=track['id'], name=track['name'], album=album_instance, artists=artist_in_a_track_list, 
                                  duration_ms=track['duration_ms'], popularity=track['popularity'])
    track_list.append(track_instance)

    # for playbacks
    spotify_playback = SpotifyPlayer(track_id=track['id'], album_id=album['id'], played_at=utils.beautify_datetime(item['played_at']))
    playback_list.append(spotify_playback)

  return artist_list, album_list, track_list, playback_list


def export_to_csv(records, filename):
  os.makedirs(f"{DATA_DIR}/{filename}", exist_ok=True) # similar to mkdir -p in linux 
  os.makedirs(f"/opt/airflow/spotify_project/data_backup/{filename}", exist_ok=True) # Create backup volume directory

  df = pd.DataFrame(records)

  # Export to host-mounted directory
  # e.g., data/track/track_ddmmyyyy_h.csv
  output_file = f"{DATA_DIR}/{filename}/{filename}_{datetime.now().strftime('%d%m%Y')}_{datetime.now().strftime('%H')}.csv"
  df.to_csv(output_file, index=False) 
  print(f"✅ Data successfully exported to: {output_file}")

  # Also export to Docker named volume for backup
  backup_file = f"/opt/airflow/spotify_project/data_backup/{filename}/{filename}_{datetime.now().strftime('%d%m%Y')}_{datetime.now().strftime('%H')}.csv"
  df.to_csv(backup_file, index=False)
  print(f"✅ Backup data successfully exported to volume: {backup_file}")



if __name__ == '__main__':
  token_info = json.load(open(TOKEN_FILE))
  recently_played = get_recently_played(token_info) # it can happen that duplicate records will be saved
  artist_list, album_list, track_list, playback_list = extract_data(recently_played)

  class_names = ["artist", "album", "track", "playback"]
  artist_list_to_csv = [artist.to_dict() for artist in artist_list]
  album_list_to_csv = [album.to_dict() for album in album_list]
  track_list_to_csv = [track.to_dict() for track in track_list]
  playback_list_to_csv = [playback.to_dict() for playback in playback_list]

  records = [artist_list_to_csv, album_list_to_csv, track_list_to_csv, playback_list_to_csv]

  for class_name, record in zip(class_names, records):
    export_to_csv(record, class_name)