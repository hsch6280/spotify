from dotenv import load_dotenv
import os
import base64
import requests
from urllib.parse import urlencode

#API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:8000/callback/'

# Spotify API endpoints
authorize_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'

scopes = [
    'user-library-read',
    'playlist-read-private',
    'playlist-read-collaborative'
]

# Encode client credentials as base64
client_creds = f'{client_id}:{client_secret}'
client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

def get_access_token(authorization_code):
    # Exchange authorization code for access token
    headers = {
        'Authorization': f'Basic {client_creds_b64}'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get('access_token')

def refresh_access_token(refresh_token):
    # Refresh access token using refresh token
    headers = {
        'Authorization': f'Basic {client_creds_b64}'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get('access_token')

def authorize_app():
    # Generate authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes)
    }
    url = authorize_url + '?' + urlencode(params)

    # Prompt user to authorize the application
    print(f'Please authorize the application by visiting:\n{url}')
    authorization_code = input('Enter the authorization code: ')

    # Get access token
    access_token = get_access_token(authorization_code)

    # Print access token and refresh token
    print(f'Access Token: {access_token}')
    refresh_token = refresh_access_token(response_data.get('refresh_token'))
    print(f'Refresh Token: {refresh_token}')

if __name__ == '__main__':
    authorize_app()
