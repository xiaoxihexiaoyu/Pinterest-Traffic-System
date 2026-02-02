#!/bin/bash

# ==============================================================================
#  File:          rename_and_unpack.sh
#  Author:        NicheGrowNerd (https://nichegrownerd.com/)
#  Description:   Extract all ZIP files in the current directory while avoiding
#                 filename conflicts and handling errors. Moves the ZIP files
#                 to the Trash after successful extraction.
#  Version:       1.1
#  Dependencies:  The script is designed to run on macOS.
#                 It requires:
#                   - unzip (installed by default on macOS)
#                   - osascript (installed by default on macOS)
#  Usage:         Copy or move this script to the same directory as the *.zip
#                 files. Make it executable (chmod +x rename_and_unpack.sh)
#                 and run it in a terminal.
# ==============================================================================

# Exit on critical errors but allow non-critical errors to show warnings
set -e

# Function to move file to macOS Trash
move_to_trash() {
    osascript -e "tell application \"Finder\" to move POSIX file \"$1\" to trash"
}

# Loop through all ZIP files in the current directory
for f in *.zip; do
    # Check if no ZIP files are found
    if [ ! -f "$f" ]; then
        echo "No .zip files found in this directory."
        break
    fi

    originalFile="$f"
    baseName="${f%.zip}"  # File name without extension
    extension="${f##*.}"  # File extension (should be "zip")

    # Remove specific problematic characters: [ ] ( )
    cleanBaseName=$(echo "$baseName" | tr -d '[]()')

    # Rename the file if necessary
    if [ "$baseName" != "$cleanBaseName" ]; then
        newFileName="$cleanBaseName.$extension"
        if [ -e "$newFileName" ]; then
            echo "Warning: The file '$newFileName' already exists. Skipping rename of '$originalFile'."
        else
            mv "$originalFile" "$newFileName"
            echo "Renamed: '$originalFile' to '$newFileName'."
            originalFile="$newFileName"
        fi
    fi

    # Define the extraction directory (same as ZIP file name)
    zipDir="${originalFile%.zip}"

    echo "Processing file: '$originalFile'"
    echo "Target directory: '$zipDir'"

    # Check if the ZIP file still exists
    if [ -f "$originalFile" ]; then
        # Only unzip if the target directory does not already exist
        if [ ! -d "$zipDir" ]; then
            unzip -o "$originalFile" -d "$zipDir" || { echo "Error: Extraction failed for '$originalFile'."; rm -rf "$zipDir"; exit 1; }
            echo "Successfully unpacked: '$originalFile' to '$zipDir'."

            # Move ZIP file to the Trash
            echo "Moving '$originalFile' to Trash..."
            if ! move_to_trash "$originalFile"; then
                echo "Warning: Could not move '$originalFile' to Trash."
            else
                echo "File '$originalFile' successfully moved to Trash."
            fi
        else
            echo "Warning: The directory '$zipDir' already exists. Skipping the ZIP file '$originalFile'."
        fi
    else
        echo "Error: The file '$originalFile' does not exist."
    fi
done

echo "Processing complete."
exit 0
