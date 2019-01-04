# Dataframe setup

import time
import json
import os
import pandas as pd

'''
Folder
'''

# Path for json folder & file
path_to_json_file = os.path.abspath('../data/json/')

# json file
json_file = '/all_trials_json' #name json file  

file = '{}{}.json'.format(path_to_json_file, json_file)

print('Paths to files and folders created')


'''
Import json into a dataframe
'''

# Clean dataframe
def clean_data():
	df = pd.read_json(file)

	print('\nJSON file read\n')

	# remove \n values
	df = df.replace(r'\n',' ', regex=True) 

	print('\nWrong n values deleted\n')

	# Rename columns
	df.columns = ['id', 
	              'submission_date',
	              'source', 
	              'brief_title', 
	              'condition', 
	              'mesh_term_condition', 
	              'mesh_term_intervention', 
	              'full_description', 
	              'summary', 
	              'city', 
	              'country', 
	              'zip']

	print('\nColumns renamed\n')
		
	# Add new date columns

	# Create new column: study_first_submitted as dates
	df['full_date'] = pd.to_datetime(df['submission_date'])

	print('\nDate column created\n')

	# Create new column: dates as year
	df['year'] = df['full_date'].dt.year

	print('\nDate as year\n')

	# Delete submission date column
	df.drop('submission_date', axis=1, inplace=True)

	# Sort records by date
	df = df.sort_values(by ='full_date')

	print('\nDATAFRAME CLEANED\n')

	filter_data(2008, df)

	export_data_csv(df)


'''
Filter data by year
'''
def filter_data(year, df):
	# Select data since 2008
	df = [df['year'] > year]

	print('\nSubset data from {}\n'.format(year))


'''
Export data as csv
'''

def export_data_csv(df, path_to_csv = os.path.abspath('../data/csv/'), csv_file = '/clean_data.csv'):
    
    try:
        os.mkdir(path_to_csv)
        print('{} created'.format(csv))
    except IOError as e:
        print(e)
        pass
    
    df.to_csv(path_to_csv + csv_file)

    print('\nCSV file exported. End of script\n')


# Functions
clean_data()

