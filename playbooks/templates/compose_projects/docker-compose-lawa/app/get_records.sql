SELECT path, time, lat, lon, make, model, lens_model FROM lawa.image_exif_enriched
WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
AND time BETWEEN %s AND %s
ORDER BY time ASC
LIMIT 50
