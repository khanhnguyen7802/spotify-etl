import os
from dotenv import load_dotenv
from flask import Flask, json, request, redirect, jsonify, session
import requests
from datetime import datetime
from app.auth.SpotifyAuth import SpotifyAuth

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_url_base = os.getenv("AUTH_URL")
api_url_base = os.getenv("API_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
app.secret_key = flask_secret_key  # for session management

spotify_auth = SpotifyAuth(client_id=client_id, client_secret=client_secret)


@app.route('/')
def index():
  if spotify_auth.access_token is not None:
    return '''
        <h1>Welcome to the Spotify API Integration!</h1>
        <a href="/playlists">Playlists</a>
        <a href="/recentlyPlayed">Recently Played</a>
    '''
  

  return '''
      <h1>Welcome to the Spotify API Integration!</h1>
      <a href="/login">Click here to login</a>
  '''

@app.route('/login')
def request_authorization():
    """
    Request authorization from the user to access Spotify resources on the user's behalf. 
    To do this, send a GET request to the /authorize endpoint. 

    :return: 
      If success, user is redirected back to the redirect_uri (contains 2 params: code and state).
      If failure, the response string contains 2 params: error and state.
    """

    auth_url = spotify_auth.request_authorization() # returns authorization URL

    return redirect(auth_url)


# only used for the first login, after that, refresh token is used to get new access tokens
@app.route('/callback')
def callback():
  """
  Handle the callback from Spotify after user authorization.
  Exchange the authorization code for an access token by sending a POST request.

  :return:
    If success, returns 200 OK and token_info (contains access_token, token_type, expires_in, refresh_token, scope).
    If failure, returns error message.  
  """
  # if failure 
  if 'error' in request.args:
      error = request.args.get("error")
      return f"Error during authorization : {error}"
  
  # if success
  if 'code' in request.args:
    token_info = spotify_auth.handle_callback(request.args.get('code'))

    if "error" in token_info: # failure
      print(token_info)
    else:
      print("Token exchanged successfully")
      session["logged_in"] = True

      with open(f"{os.getcwd()}/app/auth/auth_token.json", "w") as f:
        json.dump(spotify_auth.__dict__, f, indent=2)

    # print("Session expires at:", spotify_auth.access_token_expiration_time)

  return redirect('/')


# NOT NECESSARY IF WE MIGRATE TO AZURE VM FOR AUTOMATION 
@app.route('/refresh_token')
def refresh():
  """
  Refresh the access token using the refresh token.
  Send a POST request to the /api/token endpoint.

  :return:
    If success, returns 200 OK and new token_info (contains access_token, token_type, expires_in, scope).
    If failure, returns error message.
  """
  if spotify_auth.refresh_token is None: # refresh_token is missing, login to retrieve it
    return redirect('/login')

  if datetime.now().timestamp() > spotify_auth.access_token_expiration_time: # refresh_token is expired
    new_token_info = spotify_auth.refresh_new_token()

    if "error" in new_token_info: # failure
      print(new_token_info)
    else:
      print("Token refreshed successfully")
      
      with open(f"{os.getcwd()}/auth_token.json", "w") as f:
        json.dump(spotify_auth.__dict__, f, indent=2)

  return redirect('/')


@app.route('/playlists')
def get_playlists():
  if spotify_auth.access_token is None: # check if access_token is still valid
    return redirect('/login') # otherwise, re-login

  if datetime.now().timestamp() > spotify_auth.access_token_expiration_time: # the token is expired
    return redirect('/refresh_token') # redirect to refresh the token
   
  # get user's playlists by including the following header 
  headers = {
    "Authorization": f"Bearer {spotify_auth.access_token}"
  }

  response = requests.get(f"{api_url_base}/me/playlists", headers=headers)  # current user's playlists
  playlists = response.json()

  return jsonify(playlists)


@app.route('/recentlyPlayed')
def get_recently_played():
  if spotify_auth.access_token is None: # check if access_token is still valid
    return redirect('/login') # otherwise, re-login

  if datetime.now().timestamp() > spotify_auth.access_token_expiration_time: # the token is expired
    return redirect('/refresh_token') # redirect to refresh the token

  # get user's recently played tracks by including the following header
  headers = {
    "Authorization": f"Bearer {spotify_auth.access_token}"
  }

  response = requests.get(f"{api_url_base}/me/player/recently-played?limit=50", headers=headers) # current user's recently played tracks
  recently_played = response.json()

  return jsonify(recently_played)



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)