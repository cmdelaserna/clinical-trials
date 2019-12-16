-- Calculate number of studies over time

-- Totals
SELECT 
	year_posted, 
	sum(count(nct_id)) OVER (ORDER BY year_posted), 
	sum(count(distinct(source))) OVER (ORDER BY year_posted) as number_sources
FROM trials
GROUP BY year_posted;

-- in pre-defined table 
SELECT 
	year_posted, 
	sum(count(nct_id)) OVER (ORDER BY year_posted), 
	sum(count(distinct(source))) OVER (ORDER BY year_posted) as number_sources
FROM breastcancer
GROUP BY year_posted;


-- Number of studies with results over time
SELECT year_posted, sum(count(nct_id)) OVER (ORDER BY year_posted)
FROM trials where results = true
GROUP BY year_posted;