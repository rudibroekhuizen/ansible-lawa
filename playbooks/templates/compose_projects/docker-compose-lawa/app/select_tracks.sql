SELECT
-- formatDateTime(start_date, '%Y-%m-%d %H:%i') AS start_date,
-- formatDateTime(end_date, '%Y-%m-%d %H:%i') AS end_date,
formatDateTime(start_date, '%Y-%m-%d') AS start_date,
formatDateTime(end_date, '%Y-%m-%d') AS end_date,
description,
center_lat,
center_lon,
number_of_points
FROM lawa.trackbook_summary 
WHERE description IN ('{{ st }}');
