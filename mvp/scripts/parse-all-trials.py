'''
Clinical Trials: Parse all XML files and save data in a json file
'''

import json
import os
import xml.etree.ElementTree as ET
import shutil
import sys


'''
Create paths and folders
'''

# Folders with xml files
path_to_all_xml_trials = os.path.abspath('../data/all_trials/')

# Test folder ~100 files
path_to_test_folder = os.path.abspath('../data/test/')

# Remove old files from test folder
shutil.rmtree(path_to_test_folder)

# Path for json folder
path_to_json_file = os.path.abspath('../data/json/')

# Variable for all parsed files
all_parsed_files = []

all_folders = [path_to_all_xml_trials, path_to_test_folder, path_to_json_file]

print('\n-------------------------\n')
print('\nPaths and folders created\n')


# Check if folders exists
create_folders_errors = []

def create_folders(paths=[]):
    for p in paths:
        try:
            os.mkdir(p)
            if p:
                print('{} created'.format(p))
        except IOError as e:
            create_folders_errors.append(e)
            pass

        print('\n-------------------------\n')
        print('\nFolders created. Except: {}\n'.format(create_folders_errors))

'''
Parse all xml files and save them in all_parsed_files.
Slow. Checks for xml files
'''

def parse_xml_files(path_to_folder):
    for filename in os.listdir(path_to_folder):
        # if not filename.endswith('.xml'): continue
        fullname = os.path.join(path_to_folder, filename)
        all_parsed_files.append(ET.parse(fullname).getroot())

        # Checking message to the terminal
        print("{} file parsed\n".format(fullname))

    print('Number of files parsed: {}\n'.format(len(all_parsed_files)))

    return all_parsed_files


'''
Find values by unique tags in XML files
Save them in a dictionary
Export them to a json file
'''

all_data_dictionary = {}
print('\n-------------------------\n')
print('\nCreated al_data_dictionary\n')

def create_dictionary_from_tag(tag, parsed_files = all_parsed_files, name_dictionary = all_data_dictionary):

    # Variable to store values
    # keys = []
    values = []

    # Iterate through all xml parsed files and tags, and append data to values
    for n in parsed_files:
        for i in n.iter(tag):
            if i.text != 0:
                values.append(i.text)
            else:
                values.append('nan')
            print("{} file parsed\n".format(i.text))

    # Create dictionary and set tags as keys
    name_dictionary.setdefault(tag, [])

    # Append values to dictionary
    for i in values:
        name_dictionary[tag].append(i)
        print("{} file added to the dictionary\n".format(i))


# Function for adding new tag

def add_new_tags(new_key):
    all_data_dictionary.setdefault(new_key, [])

    for n in all_parsed_files:
            value_conditions = n.find(new_key)
            if n.find(new_key) is not None:
                all_data_dictionary[new_key].append(value_conditions.text)
            else:
                all_data_dictionary[new_key].append('None')

    print('{} tag added'.format(new_key))


# Append first condition to dictionary
# Add Nan for missing values

# all_data_dictionary.setdefault('condition', [])

# print('\nParsing conditions\n')

# for n in all_parsed_files:
#         value_conditions = n.find('condition')
#         if n.find('condition') is not None:
#             all_data_dictionary['condition'].append(value_conditions.text)
#         else:
#             all_data_dictionary['condition'].append('None')


def check_values_key():
    print('\nChecking values by key\n')

    # Check number of values by key
    for key, value in all_data_dictionary.items():
        print(key, len(list(filter(bool, value))))

'''
Export dictionary to json file
'''

# Final json file
def create_json_file():
    json_file = '/all_trials_json'

    print('\n-------------------------\n')
    print('\nCreated path to json file\n')


    # Dump dictionary into a JSON file
    print('\nExporting data to json file\n')

    with open('{}{}.json'.format(path_to_json_file, json_file), 'w') as fp:
        json.dump(all_data_dictionary, fp)
        print('JSON file created\n')

        fl = path_to_json_file + json_file
        json_size = round(os.path.getsize(fl + '.json') / 1000000, 2)
        print("JSON file: {} Mb".format(json_size))

    print('\nSCRIPT COMPLETED\n')

    sys.exit()


# Run create folders function
create_folders(all_folders)
parse_xml_files(path_to_all_xml_trials)

# Execute function for tags with single values
create_dictionary_from_tag('nct_id')
create_dictionary_from_tag('study_first_submitted')
create_dictionary_from_tag('source')
create_dictionary_from_tag('brief_title')

print('\n-----------------\n')
print('Dictionary created')

print('\n-----------------\n')
print('Adding tags')

add_new_tags('condition')
# add_new_tags('url')
add_new_tags('detailed_description/textblock')
add_new_tags('brief_summary/textblock')

check_values_key()

create_json_file()

