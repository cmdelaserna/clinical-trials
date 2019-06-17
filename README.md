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

to-do: 
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

to-do:
- timeit

#### Script 3: Clean JSON file, preprocess data
- Clean and rename columns
- Add dates columns
- Change data types
- Remove /n
- Create new column with all_text. Lowercase. Remove extra whitespace
- Remove unnecesary columns. 
- Export all_trials and word_counts datasets to sqlite database


#### Script 4: Search and visualize results
- Fetch data from sqlite db
- Search: match in all_text
- Curate context for search
	- Countvectorizer
	- tf-idf
	- Similarity between documents
- Visualize results
	- Timeline of documents. Stack by phases
	- Summary of data:
		- Main words
		- Blocks of documents (used similarity)
		- Networks of documents (similarity)

		