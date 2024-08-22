-- Task 3: Write a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
-- The table dump `metal_bands.sql` should be imported before running this script
-- The results should include the columns `band_name` and `lifespan` (in years, calculated up to 2022)
-- The script should be executable on any database

SELECT
    band_name,
    (IFNULL(split, '2022') - formed) AS lifespan
FROM
    metal_bands
WHERE
    FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY
    lifespan DESC;

-- End of Task 3 script
