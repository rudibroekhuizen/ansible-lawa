FROM postgis/postgis:15-master

RUN apt-get update && \
    apt-get install -y sudo vim curl wget jq git unzip python3-pip

# Add pg_config to path
ENV PATH="${PATH}:/usr/bin"


# Topn, hll and pgcron extension
RUN curl https://install.citusdata.com/community/deb.sh > add-citus-repo.sh && \
    bash add-citus-repo.sh && \
    apt-get -y install postgresql-15-citus-11.2

RUN apt-get install -y postgresql-15-topn postgresql-15-hll postgresql-15-pgcron


# Compile CMake for H3 geospatial extension
RUN apt-get install -y build-essential libssl-dev

RUN wget -O cmake.tar.gz https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz && \
    mkdir -p /usr/src/cmake && \
    tar -zxvf cmake.tar.gz -C /usr/src/cmake --strip-components=1 && \
    rm cmake.tar.gz && \
    cd /usr/src/cmake && \
    ./bootstrap && \
    make -j "$(nproc)" && \
    make install


# H3 geospatial extension
RUN apt-get install -y pgxnclient gcc libtool git postgresql-client-15 postgresql-server-dev-15

ARG PG_H3_VERSION=4.1.2

RUN pgxn install "h3==${PG_H3_VERSION}"


# Webdav4
RUN pip install webdav4 fsspec

# Timescaledb
#RUN curl -s https://packagecloud.io/install/repositories/timescale/timescaledb/script.deb.sh | sudo bash
#RUN apt install -y timescaledb-2-postgresql-14
##RUN timescaledb-tune --quiet --yes
