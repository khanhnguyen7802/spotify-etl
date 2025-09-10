import os
from dotenv import load_dotenv
from flask import Flask, request, redirect
import secrets
import urllib
import requests
import base64
import datetime

load_dotenv()  

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_url_base = os.getenv("AUTH_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")


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
      'redirect_uri': 'http://localhost:8888/callback',
      'scope': scope,
      'state': state
    }

    # Build the authorization URL
    auth_url = f"{auth_url_base}?{urllib.parse.urlencode(params)}"

    print(f"Authorization URL: {auth_url}")
    return redirect(auth_url)


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

    # Exchange code for tokens
    response = requests.post(
      token_url,
      data = req_body,
      headers = headers
    )

    token_info = response.json()
    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]
    token_info["refresh_token"] = token_info.get("refresh_token")
    token_info["expires_in"] = token_info.get("expires_in") # last for 3600 seconds

  return token_info


@app.route('/playlists')
def get_playlists():
   if 'access_token' not in session:
      return redirect('/login')
   
   if datetime.now().timestamp() > session["expires_at"]: # the token is expired
      return redirect('/refresh_token') # redirect to refresh the token
   
   