# Spotify Discover Weekly Backup Script

This project allows you to automatically back up your Spotify Discover Weekly playlist to an archive playlist each week. The script checks for new tracks and appends them to your archive, ensuring you never lose a track you discover.

## Prerequisites
- Python 3.x
- Spotify Developer Account (to create an app and get API credentials)

## Installation

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd weekly_backup
   ```

2. **Create a Virtual Environment**
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Setup Configuration Files

### `config.json`
Create a `config.json` file in the root directory of the project with your Spotify API credentials. You can obtain these credentials by creating a Spotify app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

**`config.json`**:
```json
{
  "CLIENT_ID": "your_spotify_client_id",
  "CLIENT_SECRET": "your_spotify_client_secret",
  "REDIRECT_URI": "http://localhost:8888/callback"
}
```
- **CLIENT_ID**: Your Spotify application's client ID.
- **CLIENT_SECRET**: Your Spotify application's client secret.
- **REDIRECT_URI**: The URI to redirect after authorization (use `http://localhost:8888/callback` for local testing).

## GitHub Actions Setup

You can automate the backup using GitHub Actions, which runs the script every week without depending on your local machine's availability.

### Set Up GitHub Secrets

1. Go to your GitHub repository, click on **Settings** -> **Secrets and variables** -> **Actions**.
2. Create the following repository secrets:
   - **`SPOTIFY_CLIENT_ID`**: Your Spotify Client ID.
   - **`SPOTIFY_CLIENT_SECRET`**: Your Spotify Client Secret.
   - **`SPOTIFY_REDIRECT_URI`**: Set this to `http://localhost:8888/callback`.

## Running the Script Locally

To run the backup script manually:

1. **Activate the Virtual Environment**
   ```sh
   source myenv/bin/activate
   ```

2. **Run the Script**
   ```sh
   python weekly_backup.py
   ```

## License
This project is licensed under the MIT License.

