import wget
import sys
import zipfile
import datetime
import os
import shutil

# Save logs, print messages in terminal

sys.stdout = open('/dev/stdout', 'w')

print('Printing messages to terminal')

'''
Setup paths to data and folders
'''

# Original data
file_to_download = 'https://clinicaltrials.gov/AllPublicXML.zip'

# Paths for folders to store data
path_zip_file = '../data/zip'

path_for_download = "../data/zip/AllPublicXML.zip"

path_dest_unzip = '../data/unzip/'

path_all_trials = '../data/all_trials/'

# Create folders for data


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


# Save zip file from clinicaltrials.gov into zip folder

print('Beginning file download with wget module')

url = 'https://clinicaltrials.gov/AllPublicXML.zip'
wget.download(url, path_for_download)

now = datetime.datetime.now()
current_download = ('\nData downloaded from clinicaltrials.gov on {}\n'.format(now.strftime("%Y-%m-%d %H:%M")))

print(current_download)


# Unzip bulk download from clinicaltrials.gov

bulk_file = '/AllPublicXML.zip'


def unzip_file(f, dest):
    print("Unzipping file...")
    data_zip = zipfile.ZipFile(f)
    data_zip.extractall(dest)
    print('----{} unzipped in {}----'.format(f, dest))


unzip_file(path_for_download + bulk_file, path_dest_unzip)


'''
Basic checks & info on files
'''

# Number of folders

folders = []

for i in os.listdir(path_dest_unzip):
    folders.append(i)

print("Number of folders: " + str(len(folders)))
print("First 5 folders: " + str(folders[0:5]))


# Calculate number of trials in unzipped file

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


data = list_files(path_dest_unzip)

print("Number of trials: " + str(len(data) - 1))


'''
Move all xml files into a folder
'''

for d in data:
    try:
        if d.endswith('.xml'):
            shutil.move(d, path_all_trials)
    except IOError as e:
        print(e)
        pass

print(str("Files moved to {}".format(path_all_trials)))


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


print("All_Trials folder: " + str(round(get_size(path_all_trials), 2)) + " Gb")
print(records[0:5])


# Remove unzip files after completing setup

try:
    shutil.rmtree(path_dest_unzip)
    print("unzip folder deleted")
except IOError as e:
    print(e)
    pass


