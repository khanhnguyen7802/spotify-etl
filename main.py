import os
import tqdm
from datetime import datetime
import json
import requests

import app.helper.utils as utils
from app.models.SpotifyAlbum import SpotifyAlbum
from app.models.SpotifyArtist import SpotifyArtist
from app.models.SpotifyPlayer import SpotifyPlayer
from app.models.SpotifyTrack import SpotifyTrack
from app.auth.SpotifyAuth import SpotifyAuth

import pandas as pd 

def init():
  """
  Initialize SpotifyAuth instance by loading existing token info from auth_token.json file.
  """
  token_info = json.load(open(f"{os.getcwd()}/app/auth/auth_token.json"))

  spotify_auth = SpotifyAuth(
    client_id=token_info.get("_client_id"),
    client_secret=token_info.get("_client_secret")
  )
  
  spotify_auth.set_token_info(
    access_token=token_info.get("_access_token"),
    refresh_token=token_info.get("_refresh_token"),
    access_token_expiration_time=token_info.get("_access_token_expiration_time")
  )

  return spotify_auth

def refresh_token(spotify_auth):
  """
  Refresh the access token using the refresh token.
  Send a POST request to the /api/token endpoint.

  :param spotify_auth: SpotifyAuth instance.
  :return:
    If success, returns 200 OK and new token_info (contains access_token, token_type, expires_in, scope).
    If failure, returns error message.
  """
  if datetime.now().timestamp() > spotify_auth.access_token_expiration_time: # refresh_token is expired
      new_token_info = spotify_auth.refresh_new_token()

      if "error" in new_token_info: # failure
        print(new_token_info)
      else:
        print("Token refreshed successfully")
        
        # TODO: check again the path on VM
        with open(f"{os.getcwd()}/auth_token.json", "w") as f:
          json.dump(spotify_auth.__dict__, f, indent=2)


def get_recently_played(token_info):
  """
  Get user's recently played tracks.

  :param token_info: Dictionary containing access token and its expiration time. 
  :return:
    If success, returns recently played tracks in JSON format.
    If failure, returns error message.
  """
  if token_info.get("_access_token") is None: # check if access_token is still valid
    return "You don't have access, please log in!", 401  # otherwise, re-login

  if datetime.now().timestamp() > token_info.get("_access_token_expiration_time"): # the token is expired
    return "Session timed out, please refresh the page or log in again.", 401  # refresh the token

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
    If failure, returns error message.
  """
  if token_info.get("_access_token") is None: # check if access_token is still valid
    return "You don't have access, please log in!", 401  # otherwise, re-login

  if datetime.now().timestamp() > token_info.get("_access_token_expiration_time"): # the token is expired
    return "Session timed out, please refresh the page or log in again.", 401  # refresh the token
  
  headers = {
    "Authorization": f"Bearer {token_info.get('_access_token')}"
  }

  response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers)
  artist_info = response.json()

  return artist_info

def export_to_csv(records, filename):
  df = pd.DataFrame(records)
  df.to_csv(f"{os.getcwd()}/data/{filename}_{datetime.now().strftime('%d%m%Y')}.csv", index=False) # ddmmyyy

def retrieve_lists():
  token_info = json.load(open(f"{os.getcwd()}/app/auth/auth_token.json"))
  
  # it can happen that duplicate records will be saved
  recent_played_tracks = get_recently_played(token_info)

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

def main():
  spotify_auth = init()
  refresh_token(spotify_auth)

  artist_list, album_list, track_list, playback_list = retrieve_lists()
  class_names = ["artist", "album", "track", "playback"]

  artist_list_to_csv = [artist.to_dict() for artist in artist_list]
  album_list_to_csv = [album.to_dict() for album in album_list]
  track_list_to_csv = [track.to_dict() for track in track_list]
  playback_list_to_csv = [playback.to_dict() for playback in playback_list]

  class_names = ["artist", "album", "track", "playback"]
  records = [artist_list_to_csv, album_list_to_csv, track_list_to_csv, playback_list_to_csv]

  for class_name, record in zip(class_names, records):
    export_to_csv(record, class_name)


if __name__ == '__main__':
  main()




    


