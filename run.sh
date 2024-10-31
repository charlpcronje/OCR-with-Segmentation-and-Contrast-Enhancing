#!/bin/bash

# Bash script to create each file, open it with code-server, and wait for user input before proceeding.

# List of files to create
FILES=(
    "ocr.py"
    "config.json"
    ".env"
    "requirements.txt"
    "README.md"
    "modules/image_segmentation.py"
    "modules/image_preprocessing.py"
    "modules/ocr_processing.py"
    "modules/logging_module.py"
    "modules/configuration.py"
    "modules/utils.py"
    "interfaces/cli_interface.py"
    "interfaces/api_interface.py"
)

# Create the base project directory if it doesn't exist
mkdir -p ocr_app
cd ocr_app

for FILE in "${FILES[@]}"; do
    # Extract the directory path
    DIR=$(dirname "$FILE")
    # Create the directory if it doesn't exist
    if [ "$DIR" != "." ]; then
        mkdir -p "$DIR"
    fi

    # Create the file
    touch "$FILE"
    echo "Created file: $FILE"

    # Open the file with code-server
    code-server "$FILE"

    # Wait for user to press enter
    read -p "Press enter to proceed to the next file..."
done

echo "All files have been created and opened."
