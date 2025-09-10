import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, jsonify, session
import secrets
import urllib
import requests
import base64
from datetime import datetime

load_dotenv()  

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")
auth_url_base = os.getenv("AUTH_URL")
api_url_base = os.getenv("API_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")


app = Flask(__name__)
app.secret_key = flask_secret_key  # for session management


@app.route('/')
def index():
    return "Welcome to the Spotify API Integration!"

@app.route('/login')
def request_authorization():
    """
    Request authorization from the user to access Spotify resources on the user's behalf. 
    To do this, send a GET request to the /authorize endpoint. 

    :return: 
      If success, user is redirected back to the redirect_uri (contains 2 params: code and state).
      If failure, the response string contains 2 params: error and state.
    """
    
    scope = 'user-library-read user-read-recently-played user-top-read playlist-read-private'
    state = secrets.token_urlsafe(16)

    params = {
      'client_id': client_id,
      'response_type': 'code',
      'redirect_uri': redirect_uri,
      'scope': scope,
      'state': state,
      'show_dialog': 'true'
    }

    # Build the authorization URL
    auth_url = f"{auth_url_base}?{urllib.parse.urlencode(params)}"

    print(f"Authorization URL: {auth_url}")


    return redirect(auth_url)


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
    req_body = {
      "code": request.args.get("code"),
      "grant_type": "authorization_code",
      "redirect_uri": redirect_uri,
    }

    # Encode client_id and client_secret in base64
    b64_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
      "Authorization": f"Basic {b64_auth}",
      "Content-Type": "application/x-www-form-urlencoded",
    }

    # Exchange code for tokens by sending POST request 
    response = requests.post(
      token_url,
      data = req_body,
      headers = headers
    )

    token_info = response.json()
    print("token info:",token_info)
    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"] # access token expires in 3600s


  return redirect('/playlists')


@app.route('/playlists')
def get_playlists():
  if 'access_token' not in session: # check if access_token is still valid
    return redirect('/login') # otherwise, re-login
   
  if datetime.now().timestamp() > session["expires_at"]: # the token is expired
    return redirect('/refresh_token') # redirect to refresh the token
   
  # get user's playlists by including the following header 
  headers = {
    "Authorization": f"Bearer {session['access_token']}"
  }
   
  response = requests.get(f"{api_url_base}/me/playlists", headers=headers) # current user's playlists
  playlists = response.json()

  return jsonify(playlists)


@app.route('/refresh_token')
def refresh_token():
  """
  Refresh the access token using the refresh token.
  Send a POST request to the /api/token endpoint.

  :return:
    If success, returns 200 OK and new token_info (contains access_token, token_type, expires_in, scope).
    If failure, returns error message.
  """
  if 'refresh_token' not in session:
    return redirect('/login')
  
  if datetime.now().timestamp() > session["expires_at"]:
    req_body = {
      "grant_type": "refresh_token",
      "refresh_token": session["refresh_token"]
    }

    # Encode client_id and client_secret in base64
    b64_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
      "Authorization": f"Basic {b64_auth}",
      "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
      token_url,
      data = req_body,
      headers = headers
    )

    new_token_info = response.json()
    session.update({
      "access_token": new_token_info["access_token"],
      "expires_at": datetime.datetime.now().timestamp() + new_token_info["expires_in"]
    })

  return redirect('/playlists')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)