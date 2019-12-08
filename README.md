# clinical-trials

- v0.2
Postgres + flask back-end. 
d3 front-end display a summary of clinical trials based on a query. 
Pubmed & clinical trials offline databases on linux pc. 

- Roadmap
v0.3 - Logic to classify trials and assess a research pipeline.
v0.4 - major bugs fixed. 
v0.5 Login system. 

### Scripts: 

#### scripts/unzip-setup.py

Summary: Download bulk zip file and unzipped files

- Bulk download (zip file) from clinicaltrials.gov
- Unzip file
- Save all xml files in a single folder
- Cleanup folder
- Time: 

to-do: 
- Remove old files before downloading a new zip file
- Save log of basic data: download date, url, time required to run script


#### scripts/parse-all-trials.py

Summary: Parse XML files, export all data as a single JSON file

- Parse files
- Extract tags with single values
- Add tags with several possible values
- Import dictionary in a dataframe
- Dump results in a JSON file
- Time: [real 166m53.614s] 


#### scripts/db setup

Summary: Import JSON file, preprocess data, export all data to sqlite as working db

- Import JSON file with all parsed data
- Data cleaning and formatting
- Create new column with all_text. 
- Create new column with recruiting label
- Export df to sqlite
- Create index in all_text for speed


### Notebooks: 
- Notebook 4: Create PostgresDB, pre-defined searches. 
- Notebook 5: Pyspark + pubmed database