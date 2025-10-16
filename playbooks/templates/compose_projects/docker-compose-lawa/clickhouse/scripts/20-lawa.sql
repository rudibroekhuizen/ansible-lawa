-- Create enriched table to get the table description
CREATE TABLE lawa.image_exif_temp
ENGINE = MergeTree
ORDER BY tuple()
AS WITH a AS
    (
        SELECT
            path,
            JSONExtract(exif_data, 'DateTimeOriginal', 'String') AS time,
            JSONExtract(exif_data, 'latitude', 'Float64') AS lat,
            JSONExtract(exif_data, 'longitude', 'Float64') AS lon,
            JSONExtract(exif_data, 'Make', 'String') AS make,
            JSONExtract(exif_data, 'Model', 'String') AS model,
            JSONExtract(exif_data, 'LensModel', 'String') AS lens_model
        FROM lawa.image_exif
    )
  SELECT
    path,
    toDateTime64(time, 6) AS time,
    lat,
    lon,
    make,
    model,
    lens_model
    -- geoToH3(lon, lat, 1) AS h3_1,
    -- geoToH3(lon, lat, 3) AS h3_3,
    -- geoToH3(lon, lat, 5) AS h3_5,
    -- geoToH3(lon, lat, 7) AS h3_7,
    -- geoToH3(lon, lat, 9) AS h3_9,
    -- geoToH3(lon, lat, 11) AS h3_11,
    -- geoToH3(lon, lat, 13) AS h3_13,
    -- geoToH3(lon, lat, 15) AS h3_15
FROM a;


-- To get the table description:
-- SHOW TABLE image_exif_temp; 


CREATE TABLE lawa.image_exif_enriched
(
    `path` String,
    `time` DateTime64(6),
    `lat` Float64,
    `lon` Float64,
    `make` String,
    `model` String,
    `lens_model` String
    -- `h3_1` UInt64,
    -- `h3_3` UInt64,
    -- `h3_5` UInt64,
    -- `h3_7` UInt64,
    -- `h3_9` UInt64,
    -- `h3_11` UInt64,
    -- `h3_13` UInt64,
    -- `h3_15` UInt64
)
ENGINE = MergeTree
ORDER BY time
SETTINGS index_granularity = 8192;


-- h3_1 -- -- -- -- --
-- Create target table h3_1
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_1;

CREATE TABLE lawa.image_exif_agg_h3_1
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_1
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_1_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_1_mv TO lawa.image_exif_agg_h3_1
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 1))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 1))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 1) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_2 -- -- -- -- --
-- Create target table h3_2
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_2;

CREATE TABLE lawa.image_exif_agg_h3_2
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_2
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_2_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_2_mv TO lawa.image_exif_agg_h3_2
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 2))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 2))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 2) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_3 -- -- -- -- --
-- Create target table h3_3
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_3;

CREATE TABLE lawa.image_exif_agg_h3_3
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_3
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_3_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_3_mv TO lawa.image_exif_agg_h3_3
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 3))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 3))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 3) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_4 -- -- -- -- --
-- Create target table h3_4
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_4;

CREATE TABLE lawa.image_exif_agg_h3_4
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_4
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_4_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_4_mv TO lawa.image_exif_agg_h3_4
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 4))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 4))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 4) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_5 -- -- -- -- --
-- Create target table h3_5
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_5;

CREATE TABLE lawa.image_exif_agg_h3_5
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_5
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_5_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_5_mv TO lawa.image_exif_agg_h3_5
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 5))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 5))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 5) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_6 -- -- -- -- --
-- Create target table h3_6
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_6;

CREATE TABLE lawa.image_exif_agg_h3_6
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_6
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_6_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_6_mv TO lawa.image_exif_agg_h3_6
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 6))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 6))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 6) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_7 -- -- -- -- --
-- Create target table h3_7
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_7;

CREATE TABLE lawa.image_exif_agg_h3_7
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_7
DROP TABLE IF EXISTS lawa.image_exif_agg_h3_7_mv;

CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_7_mv TO lawa.image_exif_agg_h3_7
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 7))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 7))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 7) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_8 -- -- -- -- --
-- Create target table h3_8
CREATE TABLE lawa.image_exif_agg_h3_8
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_8
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_8_mv TO lawa.image_exif_agg_h3_8
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 8))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 8))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 8) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_9 -- -- -- -- --
-- Create target table h3_9
CREATE TABLE lawa.image_exif_agg_h3_9
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_9
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_9_mv TO lawa.image_exif_agg_h3_9
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 9))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 9))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 9) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;


-- h3_10 -- -- -- -- --
-- Create target table h3_10
CREATE TABLE lawa.image_exif_agg_h3_10
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_10
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_10_mv TO lawa.image_exif_agg_h3_10
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 10))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 10))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 10) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;



-- h3_11 -- -- -- -- --
-- Create target table h3_11
CREATE TABLE lawa.image_exif_agg_h3_11
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_11
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_11_mv TO lawa.image_exif_agg_h3_11
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 11))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 11))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 11) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;



-- h3_12 -- -- -- -- --
-- Create target table h3_12
CREATE TABLE lawa.image_exif_agg_h3_12
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_12
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_12_mv TO lawa.image_exif_agg_h3_12
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 12))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 12))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 12) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;



-- h3_13 -- -- -- -- --
-- Create target table h3_13
CREATE TABLE lawa.image_exif_agg_h3_13
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_13
CREATE MATERIALIZED VIEW lawa.image_exif_agg_h3_13_mv TO lawa.image_exif_agg_h3_13
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 13))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 13))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 13) AS h3_cell,
    countState(*) AS cnt
FROM lawa.image_exif_enriched
GROUP BY 1, 2, 3, 4;



-- Insert data from image_exif to image_exif_enriched
INSERT INTO lawa.image_exif_enriched
WITH a AS
    (
        SELECT
            path,
            JSONExtract(exif_data, 'DateTimeOriginal', 'String') AS time,
            JSONExtract(exif_data, 'latitude', 'Float64') AS lat,
            JSONExtract(exif_data, 'longitude', 'Float64') AS lon,
            JSONExtract(exif_data, 'Make', 'String') AS make,
            JSONExtract(exif_data, 'Model', 'String') AS model,
            JSONExtract(exif_data, 'LensModel', 'String') AS lens_model
        FROM lawa.image_exif
    )
  SELECT
    path,
    toDateTime64(time, 6) AS time,
    lat,
    lon,
    make,
    model,
    lens_model
    -- geoToH3(lon, lat, 1) AS h3_1,
    -- geoToH3(lon, lat, 3) AS h3_3,
    -- geoToH3(lon, lat, 5) AS h3_5,
    -- geoToH3(lon, lat, 7) AS h3_7,
    -- geoToH3(lon, lat, 9) AS h3_9,
    -- geoToH3(lon, lat, 11) AS h3_11,
    -- geoToH3(lon, lat, 13) AS h3_13,
    -- geoToH3(lon, lat, 15) AS h3_15
FROM a;
--
