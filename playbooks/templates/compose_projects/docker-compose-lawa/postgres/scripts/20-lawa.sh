#!/bin/bash

# TODO: migrate to python using https://pypi.org/project/GDAL/

# Get database credentials from environment variables
POSTGRES_HOST=localhost
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}


## Check if a directory argument is provided
#if [ $# -eq 0 ]; then
#  echo "Error: Please specify a directory containing GPX files as an argument."
#  exit 1
#fi

# Get the directory path from the first argument
# gpx_dir="$1" # Uncomment this line and remove the hardcoded path if you want to pass the directory as an argument
gpx_dir='/tmp/trackbook' # Hardcoded for now based on your script, but consider using the argument

# Check if the directory exists
if [ ! -d "$gpx_dir" ]; then
  echo "Error: Directory '$gpx_dir' not found."
  exit 1
fi

# Loop through all files with .gpx extension in the specified directory
for file in "$gpx_dir"/*.gpx; do

  # Check if any GPX files were found (handles cases where glob doesn't match)
  if [[ -e "$file" ]]; then

    # Extract the filename without the path and extension
    filename=$(basename "$file")
    filename_no_ext="${filename%.*}"

    echo "Processing file: $file"
    echo "Adding description: '$filename_no_ext'"

    # Construct the ogr2ogr command with environment variables and the new SQL
    ogr2ogr -f "PostgreSQL" \
      PG:"host=$POSTGRES_HOST user=$POSTGRES_USER dbname=$POSTGRES_DB password=$POSTGRES_PASSWORD" \
      -nln trackbook_import \
      -sql "SELECT *, '$filename_no_ext' AS description FROM track_points" \
      "$file"

    # Informative message (optional)
    echo "Successfully processed: $file"
    echo "--------------------------------------------------"
  else
    echo "No .gpx files found in '$gpx_dir'."
    break # Exit the loop if no files were found
  fi

done
