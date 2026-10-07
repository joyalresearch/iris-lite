-- Find assets with substantial vegetation-index decline.

SELECT
    a.asset_name,
    p.before_date,
    p.after_date,
    p.mean_change,
    p.decreased_fraction,
    p.cog_path
FROM eo_change_products AS p
JOIN monitored_assets AS a
    ON p.asset_id = a.asset_id
WHERE
    p.index_name = 'NDVI'
    AND p.decreased_fraction > 0.50
ORDER BY
    p.decreased_fraction DESC;