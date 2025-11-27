import os
from dotenv import load_dotenv
import secrets
import urllib
import requests
import base64
from datetime import datetime


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_url_base = os.getenv("AUTH_URL")
api_url_base = os.getenv("API_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")


class SpotifyAuth:
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id         
        self.client_secret = client_secret
        self.access_token = None 
        self.refresh_token = None
        self.access_token_expiration_time = None
    
    # getters and setters
    @property
    def client_id(self):
        return getattr(self, "_client_id", None)

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def client_secret(self):
        return getattr(self, "_client_secret", None)

    @client_secret.setter
    def client_secret(self, value):
        self._client_secret = value

    @property
    def access_token(self):
        return getattr(self, "_access_token", None)

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def access_token_expiration_time(self):
        return getattr(self, "_access_token_expiration_time", None)

    @access_token_expiration_time.setter
    def access_token_expiration_time(self, value):
        self._access_token_expiration_time = value

    @property
    def refresh_token(self):
        return getattr(self, "_refresh_token", None)
    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = value

    def set_token_info(self, access_token, refresh_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_expiration_time = datetime.now().timestamp() + expires_in  # access token expiration time

    def request_authorization(self):
        """
        Request authorization to access Spotify. 
        To do this, send a GET request to the /authorize endpoint. 

        :return: authorization URL
        """
        
        scope = 'user-library-read user-read-recently-played user-top-read playlist-read-private'
        state = secrets.token_urlsafe(16)

        params = {
        'client_id': self.client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state,
        'show_dialog': 'true'
        }

        # Build the authorization URL
        auth_url = f"{auth_url_base}?{urllib.parse.urlencode(params)}"

        return auth_url
    
    def handle_callback(self, authorization_code):
        """
        Handle the callback from Spotify after user authorization.
        Exchange the authorization code for an access token by sending a POST request.

        :param authorization_code: authorization code received from Spotify
        :return:
            If success, returns 200 OK and token_info (contains access_token, token_type, expires_in, refresh_token, scope).
            If failure, returns error message.  
        """

        req_body = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        # Encode client_id and client_secret in base64
        b64_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Exchange code for tokens by sending POST request 
        response = requests.post(
            token_url,
            data=req_body,
            headers=headers
        )

        if response.status_code != 200:
            return f"error with handling callback with code {response.status_code}"
        
        token_info = response.json()
        self.set_token_info(
          access_token=token_info["access_token"],
          refresh_token=token_info["refresh_token"],
          expires_in=token_info["expires_in"]
        )

        return token_info

    def refresh_new_token(self):
        """
        Refresh the access token using the refresh token.
        Send a POST request to the /api/token endpoint.

        :return:
            If success, returns 200 OK and new token_info (contains access_token, token_type, expires_in, scope).
            If failure, returns error message.
        """
    
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        # Encode client_id and client_secret in base64
        b64_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            token_url,
            data = req_body,
            headers = headers
        )
    
        if response.status_code != 200:
            return f"error with refreshing token with code {response.status_code}"

        new_token_info = response.json()
        self.set_token_info(
          access_token=new_token_info["access_token"],
          refresh_token=self.refresh_token,  # remain unchanged
          expires_in=new_token_info["expires_in"]
        )

        return new_token_info
    