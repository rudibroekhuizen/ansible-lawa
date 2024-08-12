#!/bin/bash
set -euo pipefail

echo -e "Sync gpx files from remote webdav store..."
dav -u $WEBDAV_USER -p $WEBDAV_PASSWORD sync --delete dav://lawa/trackbook /var/lib/postgresql/scripts/trackbook
