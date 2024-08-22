-- Task 2: Write a SQL script that ranks country origins of bands, ordered by the number of fans
-- The table dump `metal_bands.sql` should be imported before running this script
-- The results should include the columns `origin` and `nb_fans`
-- The script should be executable on any database

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

-- End of Task 2 script
