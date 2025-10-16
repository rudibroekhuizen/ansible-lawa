#!/bin/bash
set -euo pipefail

arg=${1:-}

echo -e "Sync images from remote webdav store..."


if [[ "$arg" == "sample" ]]; then
    dav -u $WEBDAV_USER -p $WEBDAV_PASSWORD sync --delete dav://lawa/images_sample assets/images
elif [[ "$arg" == "test" ]]; then
    echo "Argument 'test' detected. Performing test operations..."
    echo "TEST_MESSAGE"
else
    dav -u $WEBDAV_USER -p $WEBDAV_PASSWORD sync --delete dav://lawa/images assets/images
fi
