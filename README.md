# clinical-trials

### Current workflow: 

#### Raw Data  [script 1]
[time required:  ]
- Bulk download (zip file) from clinicaltrials.gov
- Unzip file
- Save all xml files in a single folder
- Cleanup folder

Pending: 
- timeit
- Archive old files
- Save log of basic data: download date and time

#### Parse XML files, export all data as a single JSON file [script 2]
[time required: 2h20m ]
- Parse files
- Extract tags with single values
- Add tags with several possible values
- Import dictionary in a dataframe
- Dump results in a JSON file

Pending:
- timeit

#### ML analysis[script 3]
- Clean dataset:
	- Import JSON file, clean and rename columns
	- Add dates columns
	- Remove unnecesary columns
	- Change data types
	- Remove records before 2008
	- Save all conditions, sources and mesh_terms in lists for labeling
	- Check terms in lists for labeling
	- Create new column with title + full description
- Transformations: 
	- Text-processing: lowercasing, lemmatization, stop-word removal
	- Disease classification 
	- Computing tf-idf scores

