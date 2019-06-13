# clinical-trials


### Data sources:
- clinicaltrials.gov bulk download
- Medline Plus (https://medlineplus.gov/xml.html)
- Unified Medical Language (https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)
- Wikidocs


### Workflow: 

#### Script 1: Raw Data
[time required:  ]
- Bulk download (zip file) from clinicaltrials.gov
- Unzip file
- Save all xml files in a single folder
- Cleanup folder

Pending: 
- timeit
- Archive old files
- Save log of basic data: download date and time

#### Script 2: Parse XML files, export all data as a single JSON file
[time required: 2h20m ]
- Parse files
- Extract tags with single values
- Add tags with several possible values
- Import dictionary in a dataframe
- Dump results in a JSON file

Pending:
- timeit

#### Script 3: Clean JSON file, preprocess data
- Clean dataset:
	- Clean and rename columns
	- Add dates columns
	- Remove unnecesary columns and symbols (whitespace, /n)
	- Change data types
	- Create new column with all_text. Lowercase
- ML pre-process: 
	- Entity extraction (Scispacy) 
	- Computing tf-idf scores
- Remove unnecesary columns. 
- Export working dataset

#### Script 4: Search and visualize results