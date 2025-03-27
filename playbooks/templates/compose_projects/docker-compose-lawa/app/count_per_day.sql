SELECT toStartOfDay(time), count(*) AS cnt
FROM lawa.trackbook_enriched
WHERE 1 = 1
AND lat BETWEEN %s AND %s
AND lon BETWEEN %s AND %s
AND time BETWEEN %s AND %s
GROUP BY 1
ORDER BY 1
