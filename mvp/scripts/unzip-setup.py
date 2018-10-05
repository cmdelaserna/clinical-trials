import wget
import sys
import zipfile
import datetime
import os
import shutil

# PRINT MESSAFGES IN THE TERMINAL

sys.stdout = open('/dev/stdout', 'w')

print('\n-- Printing messages to terminal --\n')


'''
SETUP FOLDERS AND PATHS FOR all_xml_files

'''

# all_xml_files url
file_to_download = 'https://clinicaltrials.gov/AllPublicXML.zip'

# Paths for folders to store all_xml_files

path_zip_file = os.path.abspath('../data/zip')

path_for_download = os.path.abspath('../data/zip/AllPublicXML.zip')

path_dest_unzip = os.path.abspath('../data/unzip/')

path_all_trials = os.path.abspath('../data/all_trials/')


# Create folders

def create_folders(paths=[]):
    for p in paths:
        try:
            os.mkdir(p)
            if p:
                print('{} created'.format(p))
        except IOError as e:
            print(e)
            pass

    print('\nSetup folders created\n')


all_folders = [path_zip_file, path_for_download, path_dest_unzip, path_all_trials]


create_folders(all_folders)


'''
SAVE ZIP FILE FROM CLINICALTRIALS.GOV IN THE ZIP FOLDER

'''

print('Beginning file download from clinicaltrials.gov\n')

url = 'https://clinicaltrials.gov/AllPublicXML.zip'

wget.download(url, path_for_download)

now = datetime.datetime.now()
date_format = now.strftime("%Y-%m-%d %H:%M")
current_download = ('\nall_xml_files downloaded on {}\n'.format(date_format))

print(current_download)


'''
UNZIP BULF DOWNLOAD

'''

bulk_file = '/AllPublicXML.zip'


def unzip_file(f, dest):
    print("Unzipping file...\n")
    all_xml_files_zip = zipfile.ZipFile(f)
    all_xml_files_zip.extractall(dest)
    print('\n----{} unzipped in:\n{}----\n'.format(f, dest))


unzip_file(path_for_download + bulk_file, path_dest_unzip)


'''
Basic checks on files
'''

# Number of folders

folders = []

for i in os.listdir(path_dest_unzip):
    folders.append(i)

print("\nNumber of folders: {}\n".format(folders))
print("\nFirst 5 folders: {}\n".format(folders[0:5]))


# Calculate number of trials in unzipped file

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


all_xml_files = list_files(path_dest_unzip)

print("\nNumber of trials: {}".format() + str(len(all_xml_files) - 1))


'''
MOVE ALL XML FILES INTO A SINGLE FOLDER

'''

for d in all_xml_files:
    try:
        if d.endswith('.xml'):
            shutil.move(d, path_all_trials)
    except IOError as e:
        print(e)
        pass

print("\nFiles moved to {}".format(path_all_trials))


# Get all_trials numbers & size

records = []


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            records.append(f)
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / 1000000000


print("\nAll_Trials folder: " + str(round(get_size(path_all_trials), 2)) + " Gb")
print(records[0:5])


# Remove unzip files after completing setup

try:
    shutil.rmtree(path_dest_unzip)
    print("\nunzip folder deleted")
except IOError as e:
    print(e)
    pass
