import os
from dotenv import load_dotenv
from flask import Flask, json, request, redirect, jsonify, session
from flask_cors import CORS
from flasgger import Swagger
import requests
from datetime import datetime
from src.auth.SpotifyAuth import SpotifyAuth
from flask import send_file

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_url_base = os.getenv("AUTH_URL")
api_url_base = os.getenv("API_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app = Flask(__name__)
app.secret_key = flask_secret_key  # for session management
CORS(app, supports_credentials=True, origins=[frontend_url])

# Swagger Configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "WrapMySpotify API",
        "description": "API for Spotify data orchestration and analytics platform. Provides OAuth authentication and user data access.",
        "version": "1.0.0"
    },
    "host": "127.0.0.1:5000",
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "OAuth2": {
            "type": "oauth2",
            "flow": "authorizationCode",
            "authorizationUrl": "https://accounts.spotify.com/authorize",
            "tokenUrl": "https://accounts.spotify.com/api/token",
            "scopes": {
                "user-library-read": "Read user's saved content",
                "user-read-recently-played": "Access listening history",
                "user-top-read": "Read user's top artists and tracks",
                "playlist-read-private": "Access private playlists"
            }
        }
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

spotify_auth = SpotifyAuth(client_id=client_id, client_secret=client_secret)


@app.route('/')
def index():
  """
  API Home Page
  ---
  tags:
    - System
  responses:
    200:
      description: HTML page with navigation links
  """
  if spotify_auth.access_token is not None:
    return '''
        <h1>Welcome to the WrapMySpotify API! 🌯</h1>
        <ul>
            <li><a href="/api/docs">📚 View API Documentation (Swagger UI)</a></li>
            <li><a href="/confirm-download">💾 Download Your Auth Token</a></li>
            <li><a href="/login">🔐 Re-login with Spotify</a></li>
        </ul>
    '''
  

  return '''
      <h1>Welcome to the WrapMySpotify API! 🌯</h1>
      <ul>
          <li><a href="/api/docs">📚 View API Documentation (Swagger UI)</a></li>
          <li><a href="/login">🔐 Login with Spotify</a></li>
      </ul>
  '''

@app.route('/login')
def request_authorization():
    """
    Initiate Spotify OAuth Login
    ---
    tags:
      - Authentication
    summary: Initiate Spotify OAuth 2.0 authorization flow
    description: |
      Redirects the user to Spotify's authorization page to grant permissions.
      
      **OAuth Flow - Step 1:**
      1. Generates authorization URL with required scopes
      2. Includes CSRF protection state parameter
      3. Redirects user to Spotify authorization page
      4. User grants/denies permissions
      5. Spotify redirects back to /callback endpoint
      
      **Required Scopes:**
      - user-library-read: Read user's saved content
      - user-read-recently-played: Access listening history
      - user-top-read: Read user's top artists and tracks
      - playlist-read-private: Access private playlists
    responses:
      302:
        description: Redirect to Spotify authorization page
    """

    auth_url = spotify_auth.request_authorization() # returns authorization URL

    return redirect(auth_url)


# only used for the first login, after that, refresh token is used to get new access tokens
@app.route('/callback')
def callback():
  """
  OAuth Callback Handler
  ---
  tags:
    - Authentication
  summary: Handle OAuth callback from Spotify
  description: |
    Handles the OAuth callback after user authorization. This endpoint is called automatically by Spotify.
    
    **OAuth Flow - Step 2:**
    1. Receives authorization code from Spotify
    2. Exchanges code for access token and refresh token
    3. Stores tokens in auth_token.json
    4. Redirects to frontend with success/error status
  parameters:
    - name: code
      in: query
      type: string
      required: false
      description: Authorization code from Spotify
    - name: state
      in: query
      type: string
      required: false
      description: CSRF protection state parameter
    - name: error
      in: query
      type: string
      required: false
      description: Error code from Spotify if authorization failed
  responses:
    302:
      description: Redirect to frontend application with status
  """
  # if failure 
  if 'error' in request.args:
      error = request.args.get("error")
      # Redirect to frontend with error
      return redirect(f"{frontend_url}?error={error}")
  
  # if success
  if 'code' in request.args:
    token_info = spotify_auth.handle_callback(request.args.get('code'))

    if "error" in token_info: # failure
      print(token_info)
      return redirect(f"{frontend_url}?error=token_exchange_failed")
    else:
      print("Token exchanged successfully")
      
      # export token_info to a json file
      with open(f"{os.getcwd()}/src/auth/auth_token.json", "w") as f:
        json.dump(spotify_auth.__dict__, f, indent=2)
      
      # Redirect to frontend with success code (just a way to recognize successful login)
      return redirect(f"{frontend_url}?code=success")

  return redirect(frontend_url)


@app.route('/confirm-download')
def confirm_download():
  """
  Download Authentication Token File
  ---
  tags:
    - Authentication
  summary: Download auth_token.json file
  description: |
    Downloads the authentication token file containing access token, refresh token, and credentials.
    
    ⚠️ **Security Warning:**
    This file contains sensitive credentials. Use for local development only.
  responses:
    200:
      description: Token file download
      content:
        application/json:
          schema:
            type: object
  """
  token_path = f"{os.getcwd()}/src/auth/auth_token.json"
  return send_file(token_path, as_attachment=True, download_name="auth_token.json")


@app.route('/api/me')
def get_user_profile():
  """
  Get Current User Profile
  ---
  tags:
    - User
  summary: Fetch authenticated user's Spotify profile
  description: |
    Fetches the authenticated user's Spotify profile information.
    
    **Authentication Required:** Yes (valid access token)
    
    **User Information Includes:**
    - Display Name, Email, User ID
    - Account Type (free/premium)
    - Profile Images, Country, Followers
  security:
    - OAuth2: []
  responses:
    200:
      description: User profile retrieved successfully
      schema:
        type: object
        properties:
          id:
            type: string
            example: '31l77fd278dh78d'
          display_name:
            type: string
            example: 'Alex Music'
          email:
            type: string
            example: 'alex@example.com'
          country:
            type: string
            example: 'NL'
          product:
            type: string
            enum: [free, premium]
            example: 'premium'
          followers:
            type: object
            properties:
              total:
                type: integer
                example: 42
    401:
      description: Not authenticated
      schema:
        type: object
        properties:
          error:
            type: string
            example: 'Not authenticated'
  """
  if spotify_auth.access_token is None:
    return jsonify({"error": "Not authenticated"}), 401
  
  headers = {
    "Authorization": f"Bearer {spotify_auth.access_token}"
  }
  
  response = requests.get(f"{api_url_base}/me", headers=headers)
  
  if response.status_code != 200:
    return jsonify({"error": "Failed to fetch user profile"}), response.status_code
  
  return jsonify(response.json())


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)