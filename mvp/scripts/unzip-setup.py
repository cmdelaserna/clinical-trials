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

data_file = os.path.abspath('../data')
path_zip_file = os.path.abspath('../data/zip')
path_for_download = os.path.abspath('../data/zip/AllPublicXML.zip')
path_dest_unzip = os.path.abspath('../data/unzip/')
path_all_trials = os.path.abspath('../data/all_trials/')

all_folders = [data_file, path_zip_file, path_for_download, path_dest_unzip, path_all_trials]

bulk_file = '/AllPublicXML.zip'


'''
FUNCTIONS
'''

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


'''
SAVE ZIP FILE FROM CLINICALTRIALS.GOV IN THE ZIP FOLDER

'''

def save_zip_file():
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
def unzip_file(f, dest):
    print("Unzipping file...\n")
    all_xml_files_zip = zipfile.ZipFile(f)
    all_xml_files_zip.extractall(dest)
    print('\n----{} unzipped in:\n{}----\n'.format(f, dest))

'''
Basic checks on files
'''
# Number of folders

def check_files():
    folders = []

    for i in os.listdir(path_dest_unzip):
        folders.append(i)

    print("\nNumber of folders: {}\n".format(folders))
    print("\nFirst 5 folders: {}\n".format(folders[0:5]))


# Calculate number of trials in unzipped file
# Move files

def move_files():
    def list_files(dir):
        r = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                r.append(os.path.join(root, name))
        return r


    all_xml_files = list_files(path_dest_unzip)

    print("\nNumber of trials: {}".format(len(all_xml_files)))

    # Move all_xml_files
    for d in all_xml_files:
        try:
            if d.endswith('.xml'):
                shutil.move(d, path_all_trials)
        except IOError as e:
            print(e)
            pass

    print("\nFiles moved to {}".format(path_all_trials))


# Get all_trials numbers & size


def get_trials_size():
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

def remove_extra_folders():
    try:
        shutil.rmtree(path_dest_unzip)
        print("\nunzip folder deleted")
    except IOError as e:
        print(e)
        pass


# __MAIN__

create_folders(all_folders)

save_zip_file()

unzip_file(path_for_download + bulk_file, path_dest_unzip)

check_files()

move_files()

get_trials_size()

remove_extra_folders()


