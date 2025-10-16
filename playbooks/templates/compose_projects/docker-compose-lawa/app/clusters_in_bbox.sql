SELECT
  h3_cell,
  normalize_polygon(h3ToGeoBoundary(assumeNotNull(h3_cell))) AS boundary,
  -- description,
  countMerge(cnt) AS cnt,
  -- countrycode,
  -- uniqMerge(scie_uniq) AS scie_uniq
  -- uniqMerge(rec_uniq) AS rec_uniq
  -- topKMerge(10)(scie_top) AS scie_top,
  -- approx_top_kMerge(10)(scie_top_app) AS scie_top_app,
  -- topKMerge(10)(rec_top) AS rec_top
  -- untuple(arrayJoin(approx_top_kMerge(1000)(description_top_app))) AS description
  approx_top_kMerge(1000)(description_top_app) AS description_top_app
FROM {{ table }}
WHERE latitude BETWEEN {{ min_lat }} AND {{ max_lat }} AND longitude BETWEEN {{ min_lon }} AND {{ max_lon }}
AND toDate(day) BETWEEN '{{ start_date }}' AND '{{ end_date }}'
-- AND day BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d') AND parseDateTime('{{ end_date }}', '%Y-%m-%d')
-- AND day BETWEEN parseDateTime('{{ start_date }}', '%Y-%m-%d %H:%i') AND parseDateTime('{{ end_date }}', '%Y-%m-%d %H:%i')
-- AND time BETWEEN '{{ start_date }}' AND '{{ end_date }}')
GROUP BY 1, 2
ORDER BY 1 DESC;
