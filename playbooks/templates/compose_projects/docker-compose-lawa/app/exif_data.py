import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json
import clickhouse_connect
from clickhouse_connect import common
import psycopg
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ClickHouse configurations
clickhouse_db = os.getenv("CLICKHOUSE_DB")
clickhouse_host = os.getenv("CLICKHOUSE_HOST")
clickhouse_user = os.getenv("CLICKHOUSE_USER")
clickhouse_pass = os.getenv("CLICKHOUSE_PASSWORD")

# Clickhouse multi query
common.set_setting("autogenerate_session_id", False)

# Clickhouse connection
client = clickhouse_connect.get_client(
    host=clickhouse_host,
    port=8123,
    user=clickhouse_user,
    password=clickhouse_pass,
    database=clickhouse_db,
)

# Postgres vars
postgres_host = os.getenv("POSTGRES_HOST")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")


# Postgres connection
def create_connection():
    conn = psycopg.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=5432,
    )
    return conn


# Postgres connection
conn = create_connection()


def resize_images_in_directory(image_path, scale_factor=0.25):
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized_img = img.resize((new_width, new_height))

            # Resize the image
            resized_img = img.resize((new_width, new_height))

            # Save the resized image back to the same file path
            resized_img.save(image_path)

            print(f"Resized and saved: {image_path}")
    except Exception as e:
        print(f"Failed to resize {image_path}: {e}")


# Function to decode binary data
def decode_binary(tag, value):
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return value.hex()
    return value


def dms_to_decimal(degrees, minutes, seconds, reference):
    """
    Converts Degrees Minutes Seconds (DMS) coordinates to a decimal value.

    Args:
        degrees: Degrees value (int).
        minutes: Minutes value (int).
        seconds: Seconds value (float).
        reference: Hemisphere reference (e.g., 'N' or 'S').

    Returns:
        Decimal representation of the latitude/longitude.
    """
    decimal_minutes = minutes / 60 + seconds / 3600
    decimal_value = degrees + decimal_minutes

    # Handle negative values for South or West hemispheres
    if reference in ("S", "W"):
        decimal_value *= -1

    return decimal_value


def dms_to_decimal(degrees, minutes, seconds, reference):
    """Converts degrees, minutes and seconds to decimal format.

    Args:
      degrees: Integer value representing degrees.
      minutes: Integer value representing minutes.
      seconds: Float value representing seconds.
      reference: Character indicating compass direction (N, S, E or W).

    Returns:
      A float representing the decimal value of the location.
    """

    decimal = degrees + minutes / 60 + seconds / 3600
    if reference in ["S", "W"]:
        decimal = -decimal
    return decimal


def extract_metadata_and_save(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data:
            # Exclude ComponentsConfiguration, Makernote and UserComment tags
            exif_data = {
                TAGS.get(tag, tag): value
                for tag, value in exif_data.items()
                if tag not in (37121, 37500, 37510)
            }

            metadata = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                value = decode_binary(tag, value)
                metadata[tag_name] = value

            # Extract and format GPS data
            gps_info = {}
            if "GPSInfo" in exif_data:
                for key in exif_data["GPSInfo"].keys():
                    decode = GPSTAGS.get(key, key)
                    gps_info[decode] = exif_data["GPSInfo"][key]

                output_data = {}
                if all(
                    key in gps_info
                    for key in [
                        "GPSLatitude",
                        "GPSLatitudeRef",
                        "GPSLongitude",
                        "GPSLongitudeRef",
                    ]
                ):
                    degrees_lat, minutes_lat, seconds_lat = gps_info["GPSLatitude"]
                    reference_lat = gps_info["GPSLatitudeRef"]

                    degrees_lon, minutes_lon, seconds_lon = gps_info["GPSLongitude"]
                    reference_lon = gps_info["GPSLongitudeRef"]

                    decimal_latitude = dms_to_decimal(
                        int(degrees_lat),
                        int(minutes_lat),
                        float(seconds_lat),
                        reference_lat,
                    )
                    decimal_longitude = dms_to_decimal(
                        int(degrees_lon),
                        int(minutes_lon),
                        float(seconds_lon),
                        reference_lon,
                    )

                    output_data = {
                        "latitude": decimal_latitude,
                        "longitude": decimal_longitude,
                    }

            json_filename = os.path.splitext(image_path)[0] + ".metadata.json"

            merged_data = {**metadata, **output_data}

            # Save to JSON file
            with open(json_filename, "w") as json_file:
                json.dump(merged_data, json_file, indent=4, default=str)
                print(
                    f"Metadata for {os.path.basename(image_path)} written to {json_filename}"
                )

            # Insert data into clickhouse
            table_name = "lawa.image_exif"
            columns = ["path", "exif_data"]
            data = [(image_path, json.dumps(merged_data, default=str))]

            client.insert(table_name, data, column_names=columns)

            # Close the connection (optional, but recommended for proper resource management)
            # client.disconnect()

            # Insert data into postgres
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO image_exif (path, exif_data) VALUES (%s, %s)",
                    (image_path, json.dumps(merged_data, default=str)),
                )
                conn.commit()


# Directory containing the images
image_directory = "assets/images/"

# Loop over all the image files in the directory
for filename in os.listdir(image_directory):
    if filename.lower().endswith((".jpg", ".jpeg", ".JPG")):
        image_path = os.path.join(image_directory, filename)
        print(image_path)
        try:
          extract_metadata_and_save(image_path)
        except Exception as e:
          logger = logging.getLogger(__name__)
          logger.error(f"Error {e}, {image_path}")

        # resize_images_in_directory(image_path, scale_factor=0.25)
