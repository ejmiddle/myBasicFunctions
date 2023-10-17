#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: ./rename_files.sh <directory_path> <old_string> <new_string>"
    exit 1
fi

# Navigate to the directory
cd "$1" || exit 1

# Loop through and rename the files
for file in *"$2"*; do
    mv "$file" "${file//$2/$3}"
done

echo "Files have been renamed successfully."
