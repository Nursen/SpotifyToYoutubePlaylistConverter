import os
import requests
import requests_cache
import time
import json
import googleapiclient.discovery
import base64
from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# YouTube API credentials
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

credentials_cache = {}

def check_cache_exists(cache_name):
    cache_filename = f"{cache_name}.sqlite"
    return os.path.exists(cache_filename)

# Initialize the Youtube and Spotify request caches
def init_caches():
    request_cache_names = ['youtube_cache', 'spotify_cache']
    
    # Initialize the API request caches, expire after 1 day
    for cache_name in request_cache_names:
        if not check_cache_exists(cache_name):
            requests_cache.install_cache(cache_name=cache_name, backend='sqlite', expire_after=86400)
            
    # Initialize the credentials cache

# Authenticate with Spotify API and retrieve an access token
def get_spotify_access_token():
    creds = None
    access_token = None
    expires_at = None
    cache_key = 'spotify_credentials'
    creds_filepath = 'spotify_creds.json'
    
    # Check if the credentials are already in the cache or in the directory
    if cache_key in credentials_cache:
            creds = credentials_cache[cache_key]
        
    elif os.path.exists(creds_filepath):
        with open(creds_filepath, 'r') as file:
            creds = json.load(file)

    current_time = int(time.time())
    
    # If credentials are expired or don't exist, retrieve new token from API
    if not creds or not 'access_token' in creds or not 'expires_at' in creds or not creds['expires_at'] > current_time :
    
        # Perform the API request to get the access token
        print('Fetching Spotify access token from the API.')
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': 'Basic ' + b64encode(SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET)}
        data = {'grant_type': 'client_credentials'}
        response = requests.post(url, headers=headers, data=data)
        access_token = json.loads(response.text)['access_token']
        
        # Save the access token and expiration time in the cache
        expires_in = 3600  # Spotify access tokens are usually valid for 3600 seconds (1 hour)
        expires_at = int(time.time()) + expires_in
        creds = {
            'access_token': access_token,
            'expires_at': expires_at,
        }
        with open(creds_filepath, 'w') as file:
            json.dump(creds, file)
        credentials_cache.update({cache_key : creds})
            
    access_token = creds['access_token']
    return access_token

# Retrieve the list of track IDs from a Spotify playlist
def get_spotify_playlist_tracks(playlist_url):
    playlist_id = playlist_url.split('/')[-1]
    access_token = get_spotify_access_token()
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': f'Bearer {access_token}'}
    with requests_cache.CachedSession(cache_name='spotify_cache') as session:
        response = session.get(url, headers=headers)
        
    if response.from_cache:
        print('Using cached Spotify playlist tracks.')
    else:
        print('Fetching Spotify playlist tracks from the API.')
        
    tracks = json.loads(response.text)['items']
    track_ids = [track['track']['id'] for track in tracks if 'track' in track and track['track'] is not None and 'id' in track['track']]
    track_names = [track['track']['name'] for track in tracks if 'track' in track and track['track'] is not None and 'name' in track['track']]
    artist_names = [", ".join([artist['name'] for artist in track['track']['artists']]) for track in tracks if 'track' in track and track['track'] is not None and 'artists' in track['track']]

    return track_ids, track_names, artist_names

# Search for music videos on YouTube using track names
def search_youtube_music_videos(track_names, artist_names):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    video_ids = []
    
    with requests_cache.CachedSession(cache_name='youtube_cache') as session:
        for track_name, artist_name in zip(track_names, artist_names):
            # Check if the request is already in the cache
            response = session.get(f'https://www.googleapis.com/youtube/v3/search?q={track_name} {artist_name} music video&type=video&key={YOUTUBE_API_KEY}')
            if response.from_cache:
                print(f'Using cached response for track: {track_name} by {artist_name}')
            else:
                print(f'Making API request for track: {track_name} by {artist_name}')
                try:
                    search_response = youtube.search().list(
                        q=f'{track_name} {artist_name} music video',
                        part='id',
                        maxResults=1,
                        type='video'
                    ).execute()

                    if search_response.get('items'):
                        video_ids.append(search_response['items'][0]['id']['videoId'])
                except HttpError as e:
                    print(f'An error occurred: {e}')

    return video_ids

def get_youtube_credentials():
    creds = None
    cache_key = 'youtube_credentials'
    # Check if the credentials are already in the cache or in the directory
    if cache_key in credentials_cache:
        creds = credentials_cache[cache_key]
        
    elif os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        # If the credentials are not valid or don't exist, initiate the OAuth 2.0 flow
        flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', ['https://www.googleapis.com/auth/youtube'])
        creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        
    # update credentials cache and return credentials
    credentials_cache.update({cache_key: creds})
    return creds

# Create a YouTube playlist with the music videos
def create_youtube_playlist(video_ids, playlist_title):
    # Load OAuth 2.0 credentials from the client secrets file
    creds = get_youtube_credentials()
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

    #TODO: Check for existence/ conflict of playlist title before creating a new one
    # Create a new playlist
    playlist_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': playlist_title,
                'description': 'Playlist generated from Spotify.'
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
    ).execute()

    playlist_id = playlist_insert_response['id']

    #TODO: Only add videos not already in the playlist
    #TODO: Handle exceptions, particularly Quota Exceeded exception.
    # Add videos to the playlist
    for video_id in video_ids:
        youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()

    print(f'Playlist "{playlist_title}" created successfully.')
    
def b64encode(sample_string):
    return base64.b64encode(sample_string.encode('ascii')).decode('ascii')
    
# Get Spotify Playlist Name
def get_spotify_playlist_name(playlist_url):
    playlist_id = playlist_url.split('/')[-1]
    access_token = get_spotify_access_token()
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    playlist_name = json.loads(response.text)['name']
    return playlist_name


# Main script
def main():
    # Prompt the user for the Spotify playlist URL
    playlist_url = input('Enter the Spotify playlist URL: ')
    
    #Initialize Youtube and Spotify request caches
    init_caches()

    # Get the Spotify playlist name
    playlist_name = get_spotify_playlist_name(playlist_url)

    # Extract the track IDs, names, and artists from the Spotify playlist
    track_ids, track_names, artist_names = get_spotify_playlist_tracks(playlist_url)
    
    # Search for music videos on YouTube
    video_ids = search_youtube_music_videos(track_names, artist_names)

    # Create a YouTube playlist with the music videos
    create_youtube_playlist(video_ids, playlist_name)

if __name__ == '__main__':
    main()

