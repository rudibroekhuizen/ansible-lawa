SELECT toStartOfDay(time), count(*) AS cnt
FROM lawa.trackbook_enriched
WHERE 1 = 1
AND lat BETWEEN {{ min_lat }} AND {{ max_lat }}
AND lon BETWEEN {{ min_lon }} AND {{ max_lon }}
AND toDate(time) BETWEEN '{{ start_date }}' AND '{{ end_date }}'
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d') AND parseDateTime('{{ end_date }}', '%Y-%m-%d')
-- AND time BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d %H:%i') AND parseDateTime('{{ end_date }}', '%Y-%m-%d %H:%i')
GROUP BY 1
ORDER BY 1
