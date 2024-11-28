import base64
import requests
from ..config import (
    SPOTIFY_API_BASE_URL,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET
)

def get_spotify_access_token():
    """Get Spotify API access token using client credentials."""
    auth_url = 'https://accounts.spotify.com/api/token'
    encoded_auth = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode('utf-8')
    ).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {encoded_auth}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    payload = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()['access_token']
    raise Exception(f"Spotify authentication failed: {response.status_code}")

def fetch_spotify_album_data(album_name: str, artist_name: str, access_token: str) -> dict:
    """Fetch album data from Spotify API."""
    query = f"album:{album_name} artist:{artist_name}"
    search_url = f"{SPOTIFY_API_BASE_URL}/search"
    
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': query, 'type': 'album', 'market': 'US'}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Spotify API Error: {response.status_code}")
    
    albums = response.json()['albums']['items']
    if not albums:
        raise Exception("No album found on Spotify.")
    
    return albums[0]