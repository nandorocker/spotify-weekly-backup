#!/bin/bash

# Load environment variables from paths.env
source "$(dirname "$0")/paths.env"

# Navigate to the project directory and run the Python script
cd "$PROJECT_DIR"
source "${PROJECT_DIR}myenv/bin/activate"
python "${PROJECT_DIR}weekly_backup.py"
