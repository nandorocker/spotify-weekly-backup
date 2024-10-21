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

### 1. `config.json`
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

### 2. `paths.env`
Create a `paths.env` file to specify your project directory path. This keeps the absolute paths outside of the codebase, ensuring privacy and ease of sharing.

**`paths.env`**:
```sh
PROJECT_DIR=/absolute/path/to/weekly_backup/
```
- **PROJECT_DIR**: The absolute path to the project directory.

Add `paths.env` to `.gitignore` to ensure it is not committed to version control.

## Running the Script

To run the backup script:

1. **Activate the Virtual Environment**
   ```sh
   source myenv/bin/activate
   ```

2. **Run the Script**
   ```sh
   ./run_weekly_backup.sh
   ```

## Setting Up Weekly Automation

To run this script weekly, use `cron` on your Mac:

1. **Edit Cron Jobs**
   ```sh
   crontab -e
   ```

2. **Add a Cron Job**
   ```sh
   0 9 * * 1 /absolute/path/to/weekly_backup/run_weekly_backup.sh >> /absolute/path/to/weekly_backup/weekly_backup.log 2>&1
   ```
   This schedules the script to run every Monday at 9 AM.

## Troubleshooting
- Make sure your `config.json` and `paths.env` files are correctly set up.
- Ensure your Spotify application is correctly configured with the appropriate scopes.

## License
This project is licensed under the MIT License.

