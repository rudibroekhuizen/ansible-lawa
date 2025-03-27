WITH raw AS
    (
        WITH (
                WITH
                    a AS
                    (
                        SELECT [COLUMNS('h3') APPLY uniqCombined(12)] AS my_array
                        FROM lawa.image_exif_enriched
                        WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
                    ),
                    b AS
                    (
                        SELECT arrayMap(x -> abs(x - 500), my_array) AS diff
                        FROM a
                    ),
                    c AS
                    (
                        SELECT range(1, 9) AS rng
                    ),
                    d AS
                    (
                        SELECT
                            my_array,
                            diff,
                            rng
                        FROM a, b, c
                    )
                SELECT rng
                FROM d
                ARRAY JOIN
                    my_array,
                    diff,
                    rng
                ORDER BY
                    diff ASC,
                    rng DESC
                LIMIT 1
            ) AS res
        SELECT
            count(*) AS cnt,
            res,
            [h3_1, h3_3, h3_5, h3_7, h3_9, h3_11, h3_13, h3_15][res] AS h3_index
        FROM lawa.image_exif_enriched
        WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
        GROUP BY
            3,
            2
    )
  SELECT
      cnt,
      res,
      h3ToGeo(assumeNotNull(h3_index)).2 AS latitude,
      h3ToGeo(assumeNotNull(h3_index)).1 AS longitude
FROM raw
