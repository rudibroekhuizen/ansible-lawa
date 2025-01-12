#!/bin/bash
set -euo pipefail

echo -e "Sync images from remote webdav store..."
# dav -u $WEBDAV_USER -p $WEBDAV_PASSWORD sync --delete dav://lawa/images_sample assets/images
dav -u $WEBDAV_USER -p $WEBDAV_PASSWORD sync --delete dav://lawa/images assets/images
