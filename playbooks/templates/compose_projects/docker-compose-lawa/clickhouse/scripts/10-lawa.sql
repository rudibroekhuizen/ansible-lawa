-- Create table trackbook_enriched
DROP TABLE IF EXISTS lawa.trackbook_enriched;

CREATE TABLE lawa.trackbook_enriched
(
    `time` DateTime64(6),
    `ele` Float64,
    `track_seg_point_id` Int32,
    `lon` Float64,
    `lat` Float64,
    `description` String
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
ORDER BY time;


CREATE TABLE lawa.trackbook_summary
(
    `description` String,
    `start_date` DateTime64(6),
    `end_date` DateTime64(6),
    `number_of_points` Int64,
    `total_distance_meters` Float64,
    `total_distance_kilometers` Float64,
    `max_lat` Float64,
    `min_lat` Float64,
    `max_lon` Float64,
    `min_lon` Float64,
    `center_lat` Float64,
    `center_lon` Float64,
    `total_duration_seconds` Decimal(38, 19),
    `total_duration_hours` Decimal(38, 19),
    `average_speed_kmh` Float64,
    `start_lat` Float64,
    `start_lon` Float64,
    `end_lat` Float64,
    `end_lon` Float64
)
ENGINE = MergeTree
ORDER BY start_date;


INSERT INTO lawa.trackbook_summary 
SELECT * FROM postgresql(postgres, table='trackbook_summary');



-- To get the sql definition of a table retreived from postgres
-- CREATE TABLE trackbook_enriched 
-- ENGINE = MergeTree
-- ORDER BY tuple() AS
-- SELECT * FROM postgresql(postgres, table='trackbook');
-- SHOW TABLE trackbook_temp;
-- DROP TABLE trackbook_temp;


-- h3_1 -- -- -- -- --
-- Create target table h3_1
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_1;

CREATE TABLE lawa.trackbook_agg_h3_1
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_1
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_1_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_1_mv TO lawa.trackbook_agg_h3_1
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 1))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 1))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 1) AS h3_cell,
    description,
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_2 -- -- -- -- --
-- Create target table h3_2
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_2;

CREATE TABLE lawa.trackbook_agg_h3_2
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_2
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_2_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_2_mv TO lawa.trackbook_agg_h3_2
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 2))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 2))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 2) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_3 -- -- -- -- --
-- Create target table h3_3
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_3;

CREATE TABLE lawa.trackbook_agg_h3_3
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_3
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_3_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_3_mv TO lawa.trackbook_agg_h3_3
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 3))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 3))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 3) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_4 -- -- -- -- --
-- Create target table h3_4
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_4;

CREATE TABLE lawa.trackbook_agg_h3_4
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_4
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_4_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_4_mv TO lawa.trackbook_agg_h3_4
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 4))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 4))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 4) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_5 -- -- -- -- --
-- Create target table h3_5
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_5;

CREATE TABLE lawa.trackbook_agg_h3_5
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_5
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_5_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_5_mv TO lawa.trackbook_agg_h3_5
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 5))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 5))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 5) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_6 -- -- -- -- --
-- Create target table h3_6
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_6;

CREATE TABLE lawa.trackbook_agg_h3_6
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_6
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_6_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_6_mv TO lawa.trackbook_agg_h3_6
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 6))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 6))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 6) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_7 -- -- -- -- --
-- Create target table h3_7
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_7;

CREATE TABLE lawa.trackbook_agg_h3_7
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_7
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_7_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_7_mv TO lawa.trackbook_agg_h3_7
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 7))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 7))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 7) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_8 -- -- -- -- --
-- Create target table h3_8
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_8;

CREATE TABLE lawa.trackbook_agg_h3_8
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_8
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_8_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_8_mv TO lawa.trackbook_agg_h3_8
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 8))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 8))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 8) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_9 -- -- -- -- --
-- Create target table h3_9
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_9;

CREATE TABLE lawa.trackbook_agg_h3_9
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_9
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_9_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_9_mv TO lawa.trackbook_agg_h3_9
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 9))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 9))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 9) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_10 -- -- -- -- --
-- Create target table h3_10
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_10;

CREATE TABLE lawa.trackbook_agg_h3_10
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_10
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_10_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_10_mv TO lawa.trackbook_agg_h3_10
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 10))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 10))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 10) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_11 -- -- -- -- --
-- Create target table h3_11
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_11;

CREATE TABLE lawa.trackbook_agg_h3_11
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_11
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_11_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_11_mv TO lawa.trackbook_agg_h3_11
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 11))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 11))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 11) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_12 -- -- -- -- --
-- Create target table h3_12
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_12;

CREATE TABLE lawa.trackbook_agg_h3_12
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_12
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_12_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_12_mv TO lawa.trackbook_agg_h3_12
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 12))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 12))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 12) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- h3_13 -- -- -- -- --
-- Create target table h3_13
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_13;

CREATE TABLE lawa.trackbook_agg_h3_13
(
    `latitude` Float64,
    `longitude` Float64,
    `day` Date,
    `h3_cell` UInt64,
    `description` String,
    `description_uniq` AggregateFunction(uniq, String),
    `description_top_app` AggregateFunction(approx_top_k(1000), String),
    `cnt` AggregateFunction(count, String)
)
ENGINE = AggregatingMergeTree
ORDER BY (latitude, longitude, day);

-- Create mat view h3_13
DROP TABLE IF EXISTS lawa.trackbook_agg_h3_13_mv;

CREATE MATERIALIZED VIEW lawa.trackbook_agg_h3_13_mv TO lawa.trackbook_agg_h3_13
AS SELECT
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 13))).2 AS latitude,
    h3ToGeo(assumeNotNull(geoToH3(lon, lat, 13))).1 AS longitude,
    toDate(time) AS day,
    geoToH3(lon, lat, 13) AS h3_cell,
    description,  
    uniqState(description) AS description_uniq,
    approx_top_kState(1000)(description) AS description_top_app,
    countState(*) AS cnt
FROM lawa.trackbook_enriched
GROUP BY 1, 2, 3, 4, 5;


-- Populate table trackbook_enriched, source postgres
INSERT INTO lawa.trackbook_enriched SELECT
    *
    -- geoToH3(lon, lat, 1) AS h3_1,
    -- geoToH3(lon, lat, 3) AS h3_3,
    -- geoToH3(lon, lat, 5) AS h3_5,
    -- geoToH3(lon, lat, 7) AS h3_7,
    -- geoToH3(lon, lat, 9) AS h3_9,
    -- geoToH3(lon, lat, 11) AS h3_11,
    -- geoToH3(lon, lat, 13) AS h3_13,
    -- geoToH3(lon, lat, 15) AS h3_15
FROM postgresql(postgres, table='trackbook');


-- Create table image_exif
DROP TABLE IF EXISTS lawa.image_exif;

CREATE TABLE lawa.image_exif
(
    `path` String,
    `exif_data` String
)
ENGINE = MergeTree
ORDER BY ();


