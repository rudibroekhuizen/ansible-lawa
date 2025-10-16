--
\c lawa

CREATE EXTENSION IF NOT EXISTS postgis;


-- Create table to hold tracks
CREATE TABLE trackbook AS
  SELECT time, ele, track_seg_point_id, ST_X(_ogr_geometry_) AS lon, ST_Y(_ogr_geometry_) AS lat, description
  FROM trackbook_import;


-- Create table with summary/totals
CREATE TABLE trackbook_summary AS
SELECT
    description,
    MIN(time) AS start_date,
    MAX(time) AS end_date,
    COUNT(*) AS number_of_points,
    ST_Length(
        ST_MakeLine(
            _ogr_geometry_ ORDER BY track_seg_point_id
        )::geography
    ) AS total_distance_meters,
    (ST_Length(
        ST_MakeLine(
            _ogr_geometry_ ORDER BY track_seg_point_id
        )::geography
    ) / 1000.0) AS total_distance_kilometers,
    ST_YMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lat,
    ST_YMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lat,
    ST_XMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lon,
    ST_XMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lon,
    ST_Y(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lat,
    ST_X(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lon,
    EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) AS total_duration_seconds,
    (EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) / 3600.0) AS total_duration_hours,
    CASE
        WHEN EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) > 0 THEN
            (ST_Length(ST_MakeLine(_ogr_geometry_ ORDER BY track_seg_point_id)::geography) /
            EXTRACT(EPOCH FROM (MAX(time) - MIN(time)))) * 3.6
        ELSE 0
    END AS average_speed_kmh,
    (SELECT ST_Y(geom) FROM (
        SELECT _ogr_geometry_ AS geom, track_seg_point_id FROM trackbook_import
        WHERE description = T1.description ORDER BY track_seg_point_id ASC LIMIT 1
    ) AS start_point) AS start_lat,
    (SELECT ST_X(geom) FROM (
        SELECT _ogr_geometry_ AS geom, track_seg_point_id FROM trackbook_import
        WHERE description = T1.description ORDER BY track_seg_point_id ASC LIMIT 1
    ) AS start_point) AS start_lon,
    (SELECT ST_Y(geom) FROM (
        SELECT _ogr_geometry_ AS geom, track_seg_point_id FROM trackbook_import
        WHERE description = T1.description ORDER BY track_seg_point_id DESC LIMIT 1
    ) AS end_point) AS end_lat,
    (SELECT ST_X(geom) FROM (
        SELECT _ogr_geometry_ AS geom, track_seg_point_id FROM trackbook_import
        WHERE description = T1.description ORDER BY track_seg_point_id DESC LIMIT 1
    ) AS end_point) AS end_lon
FROM
    trackbook_import AS T1
GROUP BY
    description
ORDER BY
    description;


-- Create table with summary/totals
-- CREATE TABLE trackbook_summary AS
-- SELECT
--     description,
--     MIN(time) AS start_date,
--     MAX(time) AS end_date,
--     COUNT(*) AS number_of_points,
--     ST_Length(
--         ST_MakeLine(
--             _ogr_geometry_ ORDER BY track_seg_point_id
--         )::geography
--     ) AS total_distance_meters,
--     (ST_Length(
--         ST_MakeLine(
--             _ogr_geometry_ ORDER BY track_seg_point_id
--         )::geography
--     ) / 1000.0) AS total_distance_kilometers,
--     ST_YMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lat,
--     ST_YMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lat,
--     ST_XMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lon,
--     ST_XMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lon,
--     ST_Y(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lat,
--     ST_X(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lon,
--     EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) AS total_duration_seconds,
--     (EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) / 3600.0) AS total_duration_hours,
--     CASE
--         WHEN EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) > 0 THEN
--             (ST_Length(ST_MakeLine(_ogr_geometry_ ORDER BY track_seg_point_id)::geography) /
--             EXTRACT(EPOCH FROM (MAX(time) - MIN(time)))) * 3.6
--         ELSE 0
--     END AS average_speed_kmh
-- FROM
--     trackbook_import
-- GROUP BY
--     description
-- ORDER BY
--     description;
-- 
-- 
-- SELECT
--     description,
--     COUNT(*) AS number_of_points,
--     ST_Length(
--         ST_MakeLine(
--             _ogr_geometry_ ORDER BY track_seg_point_id
--         )::geography
--     ) AS total_distance_meters,
--     (ST_Length(
--         ST_MakeLine(
--             _ogr_geometry_ ORDER BY track_seg_point_id
--         )::geography
--     ) / 1000.0) AS total_distance_kilometers,
--     ST_YMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lat,
--     ST_YMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lat,
--     ST_XMax(ST_Envelope(ST_Collect(_ogr_geometry_))) AS max_lon,
--     ST_XMin(ST_Envelope(ST_Collect(_ogr_geometry_))) AS min_lon,
--     ST_Y(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lat,
--     ST_X(ST_Centroid(ST_Collect(_ogr_geometry_))) AS center_lon,
--     EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) AS total_duration_seconds,
--     (EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) / 3600.0) AS total_duration_hours,
--     CASE
--         WHEN EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) > 0 THEN
--             (ST_Length(ST_MakeLine(_ogr_geometry_ ORDER BY track_seg_point_id)::geography) /
--             EXTRACT(EPOCH FROM (MAX(time) - MIN(time)))) * 3.6
--         ELSE 0
--     END AS average_speed_kmh
-- FROM
--     trackbook_import
-- GROUP BY
--     description
-- ORDER BY
--     description;


-- Add primary key
ALTER TABLE trackbook_summary
ADD PRIMARY KEY (description);


-- Create table image exif info, records will be inserted using Python script
CREATE TABLE image_exif (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  path TEXT NOT NULL,
  exif_data JSONB
);

