--
\c lawa

CREATE EXTENSION IF NOT EXISTS postgis;


-- Create table to hold tracks
CREATE TABLE trackbook AS
  SELECT time, ele, track_seg_point_id, ST_X(_ogr_geometry_) AS lon, ST_Y(_ogr_geometry_) AS lat
  FROM trackbook_import;


-- Insert from table trackbook_import, created by gpx ogr2ogr tool
INSERT INTO trackbook
  SELECT time, ele, track_seg_point_id, ST_X(_ogr_geometry_) AS lon, ST_Y(_ogr_geometry_) AS lat
  FROM trackbook_import;


-- Store image exif info, inserted from Python script
CREATE TABLE image_exif (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  path TEXT NOT NULL,
  exif_data JSONB
);

