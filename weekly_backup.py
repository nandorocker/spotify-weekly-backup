import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import json
import hashlib
import os

# Load Spotify API credentials
def load_config():
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            print("Loaded credentials from config.json")
    except FileNotFoundError:
        # Fallback to environment variables if config.json is not available
        config = {
            'CLIENT_ID': os.getenv('CLIENT_ID'),
            'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
            'REDIRECT_URI': os.getenv('REDIRECT_URI'),
            'DISCOVER_WEEKLY_NAME': os.getenv('DISCOVER_WEEKLY_NAME'),
            'ARCHIVE_PLAYLIST_NAME': os.getenv('ARCHIVE_PLAYLIST_NAME'),
            'REFRESH_TOKEN': os.getenv('REFRESH_TOKEN')
        }
        print("Loaded credentials from environment variables")
    return config

config = load_config()

# Set default values for missing keys only if not already set
if not config.get('DISCOVER_WEEKLY_NAME'):
    config['DISCOVER_WEEKLY_NAME'] = 'Discover Weekly'
if not config.get('ARCHIVE_PLAYLIST_NAME'):
    config['ARCHIVE_PLAYLIST_NAME'] = 'Discover Weekly Archive'

# Check if all required credentials are set
required_keys = ['CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI', 'DISCOVER_WEEKLY_NAME', 'ARCHIVE_PLAYLIST_NAME', 'REFRESH_TOKEN']
missing_keys = [key for key in required_keys if not config.get(key) or config.get(key) == '']
if missing_keys:
    raise ValueError(f"Spotify credentials are not set for: {', '.join(missing_keys)}")

# Spotify API scope
SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-private'

# Spotify authentication using refresh token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    redirect_uri=config['REDIRECT_URI'],
    scope=SCOPE,
    open_browser=False,
    cache_path=None
))

sp.auth_manager.refresh_access_token(config['REFRESH_TOKEN'])
