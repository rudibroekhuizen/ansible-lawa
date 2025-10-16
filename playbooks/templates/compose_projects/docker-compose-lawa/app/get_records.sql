SELECT path, time, lat, lon, make, model FROM lawa.image_exif_enriched
WHERE lat BETWEEN {{ min_lat }} AND {{ max_lat }}
AND lon BETWEEN {{ min_lon }} AND {{ max_lon }}
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d %H:%i') AND parseDateTime('{{ end_date }}', '%Y-%m-%d %H:%i')
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d') AND parseDateTime('{{ end_date }}', '%Y-%m-%d')
AND toDate(time) BETWEEN '{{ start_date }}' AND '{{ end_date }}'
ORDER BY time ASC
LIMIT 50
