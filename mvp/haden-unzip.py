# Clinical trials: Setup

# Data: clinicaltrials.gov
# Source: wget https://clinicaltrials.gov/AllPublicXML.zip
# Date: September 14, 2018 [9pm]

# libraries
import zipfile
import time
import json
import os
import shutil

# Unzip bulk download from clinicaltrials.gov

# Create folders for data
cwd = os.getcwd()


def create_folders(name):
    try:
        os.mkdir(name)
        if name:
            print("Folder {} created".format(name))
    except IOError as e:
        print(e)
        pass


create_folders("data/all_trials")
create_folders("data/unzip")
create_folders("data/json")
create_folders("data/logs")

# paths for data
download = "data/AllPublicXML.zip"
dest = 'data/unzip/'
all_trials = 'data/all_trials/'
json_folder = 'data/json/'
logs = 'data/logs/'

# unzip bulk download from clinicaltrials.gov


def unzip_file(f, dest):
    start = time.time()
    print("Unzipping file...")
    data_zip = zipfile.ZipFile(f)
    data_zip.extractall(dest)
    end = time.time()
    performance = round((end - start) / 60, 2)
    print("File unzipped in " + str(performance) + " minutes")


unzip_file(download, dest)


# Move all trials to one single folder
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


data = list_files(dest)


print("Number of trials: " + str(len(data) - 1))

# Move all xml files into all_trials folder
filename = 'logs_moving_xml_files_to_one_folder.txt'
start = time.time()
for d in data:
    try:
        if d.endswith('.xml'):
            shutil.move(d, all_trials)
    except IOError as e:
        with open(logs + filename, 'w+') as file:
            file.write(str(e) + '/n')
        pass
end = time.time()
performance = round((end - start), 2)
print(str("Files moved to " + str(all_trials) + " in " + str(performance) + " seconds"))


# Get all_trials size
# Record variable is used later to parse XML files
records = []


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            records.append(f)
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / 1000000000


print("All_Trials folder: " + str(round(get_size(all_trials), 2)) + " Gb")
print(records[0:5])
