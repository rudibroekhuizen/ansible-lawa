#!/bin/bash

# TODO: migrate to python using https://pypi.org/project/GDAL/

# Get database credentials from environment variables
POSTGRES_HOST=localhost
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}


# Check if a directory argument is provided
if [ $# -eq 0 ]; then
  echo "Error: Please specify a directory containing GPX files as an argument."
  exit 1
fi

# Get the directory path from the first argument
gpx_dir="$1"

# Loop through all files with .gpx extension in the specified directory
for file in "$gpx_dir"/*.gpx; do

  # Construct the ogr2ogr command with environment variables
  ogr2ogr -f "PostgreSQL" \
  PG:"host=$POSTGRES_HOST user=$POSTGRES_USER dbname=$POSTGRES_DB password=$POSTGRES_PASSWORD" \
  -nln trackbook_import -sql "Select * From track_points" "$file"

  # Informative message (optional)
  echo "Successfully processed: $file"

done

