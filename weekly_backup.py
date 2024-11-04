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
            'ARCHIVE_PLAYLIST_NAME': os.getenv('ARCHIVE_PLAYLIST_NAME')
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
required_keys = ['CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI', 'DISCOVER_WEEKLY_NAME', 'ARCHIVE_PLAYLIST_NAME']
missing_keys = [key for key in required_keys if not config.get(key) or config.get(key) == '']
if missing_keys:
    raise ValueError(f"Spotify credentials are not set for: {', '.join(missing_keys)}")

# Spotify API scope
SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-private'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    redirect_uri=config['REDIRECT_URI'],
    scope=SCOPE
))

def get_playlist_id(playlist_name):
    # Retrieve the list of playlists for the current user
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        # Return the playlist ID if the name matches the given name
        if playlist['name'] == playlist_name:
            return playlist['id']
    # Return None if no matching playlist is found
    return None

def calculate_hash(track_uris):
    # Create a hash of the track URIs to uniquely identify the batch
    track_uris_string = ''.join(track_uris)
    return hashlib.md5(track_uris_string.encode()).hexdigest()

def backup_discover_weekly():
    # Get the Discover Weekly and Archive playlist IDs
    discover_weekly_id = get_playlist_id(config['DISCOVER_WEEKLY_NAME'])
    archive_playlist_id = get_playlist_id(config['ARCHIVE_PLAYLIST_NAME'])

    # Check if the Discover Weekly playlist exists
    if discover_weekly_id is None:
        print("Error: Could not find Discover Weekly playlist.")
        return

    # Check if the archive playlist exists, create it if it doesn't
    if archive_playlist_id is None:
        user_id = sp.current_user()['id']  # Get the current user's ID
        # Create a new playlist for archiving Discover Weekly
        archive_playlist = sp.user_playlist_create(user_id, config['ARCHIVE_PLAYLIST_NAME'], public=False)
        archive_playlist_id = archive_playlist['id']

    # Get tracks from Discover Weekly
    discover_weekly_tracks = sp.playlist_tracks(discover_weekly_id)['items']
    # Extract the URIs of the tracks
    track_uris = [track['track']['uri'] for track in discover_weekly_tracks]
    current_hash = calculate_hash(track_uris)

    # Get tracks from the archive playlist
    archive_tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(archive_playlist_id, offset=offset)
        archive_tracks.extend(response['items'])
        if len(response['items']) == 0:
            break
        offset += len(response['items'])
    # Extract the URIs of the archived tracks
    archive_track_uris = [track['track']['uri'] for track in archive_tracks]
    
    # Calculate existing hashes for archived batches
    batch_size = len(track_uris)
    existing_hashes = set()
    for i in range(0, len(archive_track_uris), batch_size):
        batch_uris = archive_track_uris[i:i + batch_size]
        if len(batch_uris) == batch_size:
            batch_hash = calculate_hash(batch_uris)
            existing_hashes.add(batch_hash)

    # Check if the current batch is already in the archive
    if current_hash in existing_hashes:
        print("No new tracks to add.")
        return

    # Find missing tracks
    missing_tracks = [track_uri for track_uri in track_uris if track_uri not in archive_track_uris]

    # Add only missing tracks from Discover Weekly to the archive playlist
    if missing_tracks:
        try:
            sp.playlist_add_items(archive_playlist_id, missing_tracks)
            print(f"Backing up {len(missing_tracks)} new tracks to '{config['ARCHIVE_PLAYLIST_NAME']}'.")
        except Exception as e:
            print(f"Error: Failed to back up tracks. {str(e)}")
    else:
        print("No new tracks to add.")

if __name__ == "__main__":
    backup_discover_weekly()