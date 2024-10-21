import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import json

# Load Spotify API credentials from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

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
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']
    return None

def backup_discover_weekly():
    # Get the Discover Weekly and Archive playlist IDs
    discover_weekly_id = get_playlist_id(DISCOVER_WEEKLY_NAME)
    archive_playlist_id = get_playlist_id(ARCHIVE_PLAYLIST_NAME)

    if discover_weekly_id is None:
        print("Error: Could not find Discover Weekly playlist.")
        return

    if archive_playlist_id is None:
        # Create archive playlist if it doesn't exist
        user_id = sp.current_user()['id']
        archive_playlist = sp.user_playlist_create(user_id, ARCHIVE_PLAYLIST_NAME, public=False)
        archive_playlist_id = archive_playlist['id']

    # Get tracks from Discover Weekly
    discover_weekly_tracks = sp.playlist_tracks(discover_weekly_id)['items']
    track_uris = [track['track']['uri'] for track in discover_weekly_tracks]

    # Check if the sequence of tracks has already been backed up
    archive_tracks = sp.playlist_tracks(archive_playlist_id)['items']
    archive_track_uris = [track['track']['uri'] for track in archive_tracks]

    if len(track_uris) >= 2:
        sequence_exists = False
        for i in range(len(archive_track_uris) - 1):
            if archive_track_uris[i:i + 2] == track_uris[:2]:
                sequence_exists = True
                break

        if sequence_exists:
            print("No new tracks to back up. The current Discover Weekly playlist has already been archived.")
            return

    # Add tracks to the archive playlist
    if track_uris:
        try:
            sp.playlist_add_items(archive_playlist_id, track_uris)
            print(f"Successfully backed up {len(track_uris)} tracks to '{ARCHIVE_PLAYLIST_NAME}'.")
        except Exception as e:
            print(f"Error: Failed to back up tracks. {str(e)}")
    else:
        print("No tracks found in Discover Weekly.")

if __name__ == "__main__":
    backup_discover_weekly()