-- “Calculate the ratio of applications for oncology trials to the total number of applications for each Academic site.”

SELECT  site_name,     
SUM(therapeutic_area = 'Oncology') / COUNT(*) AS oncology_rate 
FROM application WHERE site_category = 'Academic' GROUP BY site_name;

WITH first_app AS (
    SELECT site_name, MIN(created_at) AS first_date
    FROM application
    GROUP BY site_name
)


SELECT a.site_name
FROM application a
JOIN first_app f
  ON a.site_name = f.site_name
WHERE a.created_at BETWEEN f.first_date AND f.first_date + INTERVAL 14 DAY
GROUP BY a.site_name
HAVING COUNT(*) >= 10;

--run via this =>  mysql -u root -p inato_data < queries.sql
