#!/bin/bash

directory="/var/www/html/uploads"

while true; do

    find "$directory" -type f -mmin +2 -print | while IFS= read -r file; do
        filename=$(basename "$file")
        echo "Deleting $filename"
        rm "$file"
    done
    sleep 60
done
