import os
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

def init():
  """
  Initialize SpotifyAuth instance by loading existing token info from auth_token.json file.
  """
  token_info = json.load(open(TOKEN_FILE))

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
        
        with open(TOKEN_FILE, "w") as f:
          json.dump(spotify_auth.__dict__, f, indent=2)


# if __name__ == '__main__':
#   spotify_auth = init()
#   refresh_token(spotify_auth)
