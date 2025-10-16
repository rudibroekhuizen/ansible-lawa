SELECT description, start_lat, start_lon FROM lawa.trackbook_summary
WHERE start_lat BETWEEN {{ min_lat }} AND {{ max_lat }}
AND start_lon BETWEEN {{ min_lon }} AND {{ max_lon }}
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d %H:%i') AND parseDateTime('{{ end_date }}', '%Y-%m-%d %H:%i')
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d') AND parseDateTime('{{ end_date }}', '%Y-%m-%d')
AND toDate(start_date) BETWEEN '{{ start_date }}' AND '{{ end_date }}'
ORDER BY start_date ASC
LIMIT 50
