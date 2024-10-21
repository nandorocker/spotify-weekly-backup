import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import json
import hashlib

# Load Spotify API credentials from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Spotify API credentials
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']
SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-private'

# Playlist details
DISCOVER_WEEKLY_NAME = "Discover Weekly"
ARCHIVE_PLAYLIST_NAME = "testlist"

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
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
    discover_weekly_id = get_playlist_id(DISCOVER_WEEKLY_NAME)
    archive_playlist_id = get_playlist_id(ARCHIVE_PLAYLIST_NAME)

    # Check if the Discover Weekly playlist exists
    if discover_weekly_id is None:
        print("Error: Could not find Discover Weekly playlist.")
        return

    # Check if the archive playlist exists, create it if it doesn't
    if archive_playlist_id is None:
        user_id = sp.current_user()['id']  # Get the current user's ID
        # Create a new playlist for archiving Discover Weekly
        archive_playlist = sp.user_playlist_create(user_id, ARCHIVE_PLAYLIST_NAME, public=False)
        archive_playlist_id = archive_playlist['id']

    # Get tracks from Discover Weekly
    discover_weekly_tracks = sp.playlist_tracks(discover_weekly_id)['items']
    # Extract the URIs of the tracks
    track_uris = [track['track']['uri'] for track in discover_weekly_tracks]

    # Get tracks from the archive playlist
    archive_tracks = sp.playlist_tracks(archive_playlist_id)['items']
    # Extract the URIs of the archived tracks
    archive_track_uris = [track['track']['uri'] for track in archive_tracks]

    # Find missing tracks
    missing_tracks = [track_uri for track_uri in track_uris if track_uri not in archive_track_uris]

    # Add only missing tracks from Discover Weekly to the archive playlist
    if missing_tracks:
        try:
            sp.playlist_add_items(archive_playlist_id, missing_tracks)
            print(f"Successfully backed up {len(missing_tracks)} new tracks to '{ARCHIVE_PLAYLIST_NAME}'.")
        except Exception as e:
            # Print an error message if adding tracks fails
            print(f"Error: Failed to back up tracks. {str(e)}")
    else:
        print("No new tracks to add. The current Discover Weekly playlist has already been archived.")

if __name__ == "__main__":
    backup_discover_weekly()
