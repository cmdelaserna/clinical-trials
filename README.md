# clinical-trials

### Current workflow: 
#### Raw Data  [script 1]
- Download bulk zip data from clinicaltrials.gov
- Unzip file
- Save all xml files in a single folder

—pending debugging—

#### Parse files, export a single JSON file [script 2]
- Parse files
- Extract tags with single values
- Add tags with several possible values
- Dump results in a JSON file

#### Dataframe setup [script 3]
- Import JSON file, clean and rename columns
- Add dates columns
- Select data since 2008 (*not working)
- Export data as csv

#### ML pipeline [script 4]
- Load csv file
- Clean dataset:
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
