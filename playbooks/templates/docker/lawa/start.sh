#!/bin/bash
set -euo pipefail

echo -e "Start data containers..."
docker compose up -d clickhouse postgres

sleep 10

echo -e "Start app..."
docker compose up -d app

echo -e "Create extension Postgis..."
docker compose exec postgres bash -c 'psql -v ON_ERROR_STOP=1 -U postgres < /var/lib/postgresql/scripts/10-lawa.sql'

echo -e "Retrieve .gpx files from webdav store..."
docker compose exec postgres bash -c '/var/lib/postgresql/scripts/sync_data_store.sh'

echo -e "Import .gpx tracks into table..."
docker compose exec postgres bash -c '/var/lib/postgresql/scripts/20-lawa.sh'

echo -e "Enrich gpx data..."
docker compose exec postgres bash -c 'psql -v ON_ERROR_STOP=1 -U postgres < /var/lib/postgresql/scripts/30-lawa.sql'

echo -e "Setup tables Clickhouse..."
docker compose exec clickhouse bash -c '/var/lib/clickhouse/user_files/10-lawa.sh'

echo -e "Retrieve images from webdav store into app..."
docker compose exec app bash -c '/app/sync_data_store.sh'

echo -e "Read metadata from images..."
docker compose exec app python exif_data.py

echo -e "Enrich image data..."
docker compose exec clickhouse bash -c '/var/lib/clickhouse/user_files/20-lawa.sh'
