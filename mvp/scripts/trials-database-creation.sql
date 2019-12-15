-- Queries to create database

-- Update db. From terminal
pg_restore -e -v -x -d aact --clean --no-owner ~/Downloads/postgres_data.dmp

alter role your-username in database aact set search_path = ctgov, public;

-- Create trials table
CREATE TABLE trials as
SELECT 
    nct_id, 
    phase, 
    study_first_submitted_date, 
    study_first_submitted_qc_date,
    "study_first_submitted_qc_date"::date - "study_first_submitted_date"::date AS submitted_to_qc,
    study_first_posted_date,
    results_first_submitted_date is not null as results,
    study_type,
    overall_status,
    why_stopped is not null as stopped,
    why_stopped,
    has_expanded_access is true as has_expanded_access,
    is_fda_regulated_drug,
    is_fda_regulated_device,
    is_unapproved_device,
    official_title,
    acronym,
    source
    FROM ctgov.studies;

--
-- Add column with brief_description

-- SELECT 
--  	nct_id, 
--    'not in summaries' as note 
-- FROM 
--    trials 
-- EXCEPT
--    SELECT 
--     nct_id, 
--     'not in summaries' as note 
--   FROM 
--     ctgov.brief_summaries;

ALTER TABLE trials
ADD COLUMN description text;

UPDATE trials AS t1 
SET description = t2.description
FROM brief_summaries AS t2
WHERE t1.nct_id = t2.nct_id;


-- Add column with mesh_terms
ALTER TABLE trials
ADD COLUMN mesh_terms text;

CREATE TABLE all_mesh_terms as
select 
	nct_id,
	STRING_AGG (downcase_mesh_term, ',') mesh_terms
from 
	ctgov.browse_conditions
group by 
	nct_id;

UPDATE trials AS t1 
SET mesh_terms = t2.mesh_terms
FROM all_mesh_terms AS t2
WHERE t1.nct_id = t2.nct_id

-- Create column with all interventions
ALTER TABLE trials
ADD COLUMN interventions text;

CREATE TABLE all_interventions as
select 
	nct_id,
	STRING_AGG (downcase_mesh_term, ',') mesh_terms
from 
	ctgov.browse_interventions
group by 
	nct_id;

UPDATE trials AS t1 
SET interventions = t2.names
FROM all_interventions AS t2
WHERE t1.nct_id = t2.nct_id

-- Add recruiting_status
ALTER TABLE trials
ADD COLUMN recruiting_status text;

UPDATE trials
SET recruiting_status = CASE
WHEN overall_status = 'Recruiting' or overall_status = 'Not yet recruiting' THEN 1 ELSE 0 END

ALTER TABLE trials
ALTER COLUMN recruiting_status TYPE bool USING recruiting_status::boolean;

-- Create all_text column
ALTER TABLE trials
ADD COLUMN all_text text;

** pending query

-- Create posted year column
ALTER TABLE trials
ADD COLUMN year_posted text;

UPDATE trials SET year_posted = EXTRACT (YEAR FROM "study_first_submitted_qc_date");

ALTER TABLE trials ALTER COLUMN year_posted TYPE integer USING year_posted::integer;

-- Create search_term table

CREATE TABLE search_terms(
search_term TEXT UNIQUE NOT NULL,
return_table VARCHAR (50) NOT NULL);

ALTER TABLE search_terms ADD PRIMARY KEY (search_term);

-- Insert data manually
INSERT INTO search_terms (search_term, return_table)
VALUES ( 'breast cancer', 'breastcancer');

-- Search and create table from query
CREATE TABLE celiac
as
select * from trials
where to_tsvector(description) @@ to_tsquery('celiac | gluten');

CREATE TABLE breastcancer
as
select * from trials
where to_tsvector(description) @@ to_tsquery('breast & cancer');




