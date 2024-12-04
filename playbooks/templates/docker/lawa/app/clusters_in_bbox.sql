WITH raw AS
    (
        WITH optimal_resolution AS (
                WITH
                    a AS
                    (
                        SELECT [COLUMNS('h3') APPLY uniqCombined(12)] AS my_array
                        FROM trackbook_enriched
                        WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
                    ),
                    b AS
                    (
                        SELECT arrayMap(x -> abs(x - 500), my_array) AS diff
                        FROM a
                    ),
                    c AS
                    (
                        SELECT range(1, 9) AS range_index
                    ),
                    d AS
                    (
                        SELECT
                            my_array,
                            diff,
                            range_index
                        FROM a, b, c
                    )
                SELECT range_index
                FROM d
                ARRAY JOIN
                    my_array,
                    diff,
                    range_index
                ORDER BY
                    diff ASC,
                    range_index DESC
                LIMIT 1
            )
        SELECT
            count(*) AS cnt,
            range_index,
            [h3_1, h3_3, h3_5, h3_7, h3_9, h3_11, h3_13, h3_15][range_index] AS h3_index
        FROM trackbook_enriched, optimal_resolution
        WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s
        GROUP BY
            3,
            2
    )
  SELECT
      cnt,
      range_index,
      h3ToGeo(assumeNotNull(h3_index)).2 AS latitude,
      h3ToGeo(assumeNotNull(h3_index)).1 AS longitude
FROM raw
