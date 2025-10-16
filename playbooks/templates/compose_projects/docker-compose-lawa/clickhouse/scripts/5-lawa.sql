-- Create database
CREATE DATABASE IF NOT EXISTS lawa;

CREATE FUNCTION IF NOT EXISTS normalize_polygon AS (polygon) -> if((arrayExists(point -> ((point.2) < -90), polygon) AND arrayExists(point -> ((point.2) >= 90), polygon)), arrayMap(point -> (point.1, if((point.2) < 0, (point.2) + 360, point.2)), polygon), polygon);
