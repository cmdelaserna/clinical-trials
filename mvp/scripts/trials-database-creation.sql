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


 -- Add column with brief_description
 SELECT 
 	nct_id, 
   'not in summaries' as note 
FROM 
   trials 
EXCEPT
   SELECT 
    nct_id, 
    'not in summaries' as note 
  FROM 
    ctgov.brief_summaries;

ALTER TABLE trials
ADD COLUMN description text;

UPDATE trials AS t1 
SET description = t2.brief_summaries
FROM brief_summaries AS t2
WHERE t1.nct_id = t2.nct_id


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
SET interventions = t2.mesh_terms
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


