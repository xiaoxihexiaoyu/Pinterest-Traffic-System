#!/bin/bash

# ==============================================================================
#  File:          shuffle_and_rename_files_in_subfolders.sh
#  Author:        NicheGrowNerd (https://nichegrownerd.com/)
#  Created:       2025
#  Description:   This script recursively processes all subdirectories and
#				  renames all files within them. 
#  Version:       1.1
#  Dependencies:  This script is designed to run in a macOS terminal (bash).
#                 It requires macOS with AppleScript support for moving files
#				  to Trash. The 'unzip' command must be available
#				  (pre-installed on macOS).
#  Usage:         Copy this script to the directory containing the image folders,
#                 Make it executable (chmod +x shuffle_and_rename_files_in_subfolders.sh)
#                 and run it in a terminal.
# ==============================================================================

# Exclude this script from processing
MASTER_SCRIPT=$(basename "$0")

# Function for renaming files in a directory
rename_files() {
    echo
    echo "Processing directory: $(pwd)"

    # Get the current folder name
    FOLDER_NAME=$(basename "$(pwd)")

    # Create a temporary file to save the file names
    TEMP_FILE=$(mktemp)

    # Find all files in the current directory, excluding the script itself
    FILES=(*)
    FILE_COUNT=0

    for FILE in "${FILES[@]}"; do
        if [[ "$FILE" != "$MASTER_SCRIPT" && -f "$FILE" ]]; then
            echo "$FILE" >> "$TEMP_FILE"
            ((FILE_COUNT++))
        fi
    done

    echo "Files found for renaming: $FILE_COUNT"

    # Check if there are files to rename
    if [[ "$FILE_COUNT" -eq 0 ]]; then
        echo "No files to rename in this directory."
        return
    fi

    # Shuffle file names using sort -R
    SHUFFLED_FILE="${TEMP_FILE}_shuffled"
    sort -R "$TEMP_FILE" > "$SHUFFLED_FILE"

    # Counter for new file names
    COUNT=1

    # Iterate over the shuffled file names and rename them
    echo "Start renaming the files..."
    while IFS= read -r OLD_NAME; do
        EXT="${OLD_NAME##*.}"
        NEW_NAME="${FOLDER_NAME} ${COUNT}.${EXT}"
        
        echo "Rename from '$OLD_NAME' to '$NEW_NAME'"
        mv "$OLD_NAME" "$NEW_NAME"
        
        ((COUNT++))
    done < "$SHUFFLED_FILE"

    # Delete the temporary files
    rm -f "$TEMP_FILE" "$SHUFFLED_FILE"

    echo "Files have been successfully renamed in this directory."
}

# Recursive run through all subdirectories
echo "Start processing all subdirectories..."

find . -type d | while IFS= read -r DIR; do
    echo "Processing subdirectory: $DIR"
    cd "$DIR" || continue
    rename_files
    cd - > /dev/null || exit
done

# Also edit the current directory
rename_files

echo
echo "All directories have been processed."
read -p "Press [Enter] to exit..."
