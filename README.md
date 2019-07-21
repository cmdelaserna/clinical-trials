# clinical-trials


### Data sources:
- v0.3
-- clinicaltrials.gov bulk download (v.03)

- v0.5
-- Medline Plus (https://medlineplus.gov/xml.html)
-- Unified Medical Language (https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)
-- Wikidocs

### Workflow: 

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


#### scripts/dataframe-setup.py

Summary: Import JSON file, preoprocess data, export to sqlite as working db

- Import JSON file with all parsed data
- Clean and rename columns
- Add dates columns
- Change data types
- Remove /n
- Create new column with all_text. Lowercase. Remove extra whitespace
- Remove unnecesary columns 
- Define schema and create working db (sqlite)
- Create index for sqlite db


#### scripts/ml-analysis.py

Summary: [pending]


to-do: Extract entities from all data. Extract topics from each file? 



#### Flask APP
- Build query, search for matching string. 
- Function to add missing years in time-based charts. 
- Calculate Trial Index based on search results.
- Extract topics from search results (in preprocess?)
- Pass data to front-end (decide on datasets)


