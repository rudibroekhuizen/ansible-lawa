SELECT
  year,
  --countrycode,
  --uniqMerge(h3_5_uniq) AS h3_5_uniq,
  --uniqMerge(h3_7_uniq) AS h3_7_uniq,
  --uniqMerge(h3_9_uniq) AS h3_9_uniq
  --uniqHLL12Merge(scie_uniq_hll) AS scie_uniq_hll,
  --topKMerge(10)(scie_top) AS scie_top,
  --approx_top_kMerge(10)(scie_top_app) AS scie_top_app,
  --topKMerge(10)(rec_top) AS rec_top
  --approx_top_kMerge(10)(rec_top_app) AS rec_top_app

{% if mode == 'recordedby' %}
    countMerge(cnt) AS cnt
{% elif mode == 'scientificname' %}
    uniqMerge(scie_uniq) AS scie_uniq
{% endif %}

FROM db1.agg_gbif
WHERE 1 = 1
AND h3ToGeo(assumeNotNull(h3_2)).2 BETWEEN %s AND %s
AND h3ToGeo(assumeNotNull(h3_2)).1 BETWEEN %s AND %s
AND year BETWEEN %s AND %s
GROUP BY 1
ORDER BY 1
