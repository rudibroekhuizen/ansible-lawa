SELECT path, time, lat, lon, make, model, lens_model FROM image_exif_enriched
WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
{% if recordedby %}
AND match(lower(arrayStringConcat(recordedby.array_element)), lower('{{ recordedby }}'))
{% endif %}
ORDER BY time ASC
LIMIT 100
