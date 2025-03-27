-- Create table trackbook_enriched
CREATE TABLE lawa.trackbook_enriched
(
    `time` DateTime64(6),
    `ele` Float64,
    `track_seg_point_id` Int32,
    `lon` Float64,
    `lat` Float64,
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
ORDER BY time;


--Get sql definition of table in postgres
--CREATE TABLE trackbook_psql AS
--SELECT * FROM postgresql(postgres, table='trackbook');
--SHOW TABLE trackbook_temp;
--DROP TABLE trackbook_temp;


-- Populate table trackbook_enriched, source postgres
INSERT INTO lawa.trackbook_enriched SELECT
    *,
    geoToH3(lon, lat, 1) AS h3_1,
    geoToH3(lon, lat, 3) AS h3_3,
    geoToH3(lon, lat, 5) AS h3_5,
    geoToH3(lon, lat, 7) AS h3_7,
    geoToH3(lon, lat, 9) AS h3_9,
    geoToH3(lon, lat, 11) AS h3_11,
    geoToH3(lon, lat, 13) AS h3_13,
    geoToH3(lon, lat, 15) AS h3_15
FROM postgresql(postgres, table='trackbook');


-- Create table image_exif
CREATE TABLE lawa.image_exif
(
    `path` String,
    `exif_data` String
)
ENGINE = MergeTree
ORDER BY ();


