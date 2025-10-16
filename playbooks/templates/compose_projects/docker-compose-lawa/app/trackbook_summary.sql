WITH a AS (
SELECT
  approx_top_kMerge(1000)(description_top_app) AS description_top_app
FROM 
{{ table }}
WHERE latitude BETWEEN {{ min_lat }} AND {{ max_lat }} AND longitude BETWEEN {{ min_lon }} AND {{ max_lon }}
AND toDate(day) BETWEEN '{{ start_date }}' AND '{{ end_date }}'
-- AND day BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d') AND parseDateTime('{{ end_date }}', '%Y-%m-%d')
), b AS (
SELECT *, untuple(arrayJoin(description_top_app)) AS description FROM a
)
SELECT
description,
formatDateTime(start_date, '%Y-%m-%d %H:%i') AS start_date,
formatDateTime(end_date, '%Y-%m-%d %H:%i') AS end_date,
--formatDateTime(start_date, '%Y-%m-%d') AS start_date,
--formatDateTime(end_date, '%Y-%m-%d') AS end_date,
total_distance_kilometers,
total_duration_hours,
average_speed_kmh,
number_of_points
FROM lawa.trackbook_summary
WHERE description IN (
  SELECT description.item
  FROM b
);
