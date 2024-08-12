

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
    lens_model,
    geoToH3(lon, lat, 1) AS h3_1,
    geoToH3(lon, lat, 3) AS h3_3,
    geoToH3(lon, lat, 5) AS h3_5,
    geoToH3(lon, lat, 7) AS h3_7,
    geoToH3(lon, lat, 9) AS h3_9,
    geoToH3(lon, lat, 11) AS h3_11,
    geoToH3(lon, lat, 13) AS h3_13,
    geoToH3(lon, lat, 15) AS h3_15
FROM a;


-- To get the table description:
--SHOW TABLE image_exif_temp; 


CREATE TABLE lawa.image_exif_enriched
(
    `path` String,
    `time` DateTime64(6),
    `lat` Float64,
    `lon` Float64,
    `make` String,
    `model` String,
    `lens_model` String,
    `h3_1` UInt64,
    `h3_3` UInt64,
    `h3_5` UInt64,
    `h3_7` UInt64,
    `h3_9` UInt64,
    `h3_11` UInt64,
    `h3_13` UInt64,
    `h3_15` UInt64
)
ENGINE = MergeTree
ORDER BY time
SETTINGS index_granularity = 8192;


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
    lens_model,
    geoToH3(lon, lat, 1) AS h3_1,
    geoToH3(lon, lat, 3) AS h3_3,
    geoToH3(lon, lat, 5) AS h3_5,
    geoToH3(lon, lat, 7) AS h3_7,
    geoToH3(lon, lat, 9) AS h3_9,
    geoToH3(lon, lat, 11) AS h3_11,
    geoToH3(lon, lat, 13) AS h3_13,
    geoToH3(lon, lat, 15) AS h3_15
FROM a;
--
