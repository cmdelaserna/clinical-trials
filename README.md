# clinical-trials

### Current workflow: 
#### Raw Data  [script 1]
- Download bulk zip data
- Unzip file
- Save all xml files in a single folder

#### Parse files, export a single JSON file [script 2]
- Parse files
- Extract tags with single values
- Add tags with several values
- Dump results in a JSON file

#### Dataframe setup [script 3]
- Import JSON file, clean and rename columns
- Add dates columns
- Select data since 2008
- Export data as csv

#### ML pipeline [script 4]
- 