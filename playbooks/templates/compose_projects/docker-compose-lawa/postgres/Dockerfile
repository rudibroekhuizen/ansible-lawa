FROM postgis/postgis:15-3.7

RUN apt-get update && \
    apt-get install -y sudo vim curl wget jq git unzip python3-pip gdal-bin

# Add pg_config to path
ENV PATH="${PATH}:/usr/bin"

# Webdav4
RUN pip install --break-system-packages webdav4 fsspec

