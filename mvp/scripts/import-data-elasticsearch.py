from elasticsearch import Elasticsearch, helpers
import sys
import json
import os

es = Elasticsearch()

#confirm ES is running
res = requests.get('http://localhost:9200')

dirpath = '../data/json/'

filename = 'all_trials_json.json'


def load_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(directory+filename,'r') as open_file:
                yield json.load(open_file)

load_json(dirpath)

helpers.bulk(es, load_json(dirpath), index='clinical-trials', doc_type='document')