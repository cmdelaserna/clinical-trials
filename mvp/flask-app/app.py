# FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
# To React: https://realpython.com/the-ultimate-flask-front-end/
#
#Configuration
#

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
import json
import numpy as np

'''
CONFIGURATION
'''
app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE = '../data/working_data/database.db'


'''
FUNCTIONS
'''

# BUILD QUERY
def build_query(search_field):
   # Global variables
   global search, full_query_string
   search = request.form   

   # Build query
   result_value = request.form[search_field]
   first_sql = "SELECT * from all_trials WHERE all_text LIKE "
   term = "'%" + str(result_value) + "%'"

   full_query_string = first_sql + term

   return full_query_string


# ADD MISSING YEARS IN TIME-BASED CHARTS
def add_missing_years(data, column_year, column_name_count):

   global df_year_final

   all_years = np.arange(1999, 2020)
   zeros = ([0] * len(all_years))
   missing_years = [item for item in all_years if item not in data]
   columns = [column_year, column_name_count] #ie, ['year_submitted', 'nct_id']

   zippedList =  list(zip(missing_years, zeros))
   df_all_years = pd.DataFrame(zippedList, columns = columns) 

   df_year_final = pd.concat([data, df_all_years], ignore_index=True)
   df_year_final = df_year_final.sort_values(by=column_year).reset_index(drop=True)

   return df_year_final


# ADD MISSING YEARS IN TRIALS BY PHASE
def phase_missing_years(data, column_year, column_phase, column_name_count):

   global df_phase_final

   all_years = np.arange(1999, 2020)
   zeros = ([0] * len(all_years))
   missing_years = [item for item in all_years if item not in data]
   columns = [column_year, column_phase, column_name_count] #ie, ['year_submitted', 'nct_id']

   zippedList =  list(zip(missing_years, zeros, zeros))
   df_all_years = pd.DataFrame(zippedList, columns = columns) 

   df_phase_final = pd.concat([data, df_all_years], ignore_index=True)
   df_phase_final = df_phase_final.sort_values(by=column_year).reset_index(drop=True)

   return df_phase_final


'''
VIEWS
'''

# Index
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
   return render_template('index.html')

# Results
@app.route('/result', methods = ['GET', 'POST'])
def search():
   if request.method == 'POST':

      #Connect to db
      conn = sqlite3.connect(DATABASE)      

      # # Query, store data
      build_query('Search')
      df = pd.read_sql_query(full_query_string, conn)
      number_results = len(df)

      # Group by year
      df_year = df.groupby(['year_submitted'], as_index=False).nct_id.count()
      add_missing_years(df_year, 'year_submitted', 'nct_id')

      # Get number of sources in query
      df_source = df.groupby(['source'], as_index=False).nct_id.count()
      source_number = df_source['source'].nunique()

      # Trials by phase, year
      df_phase = df.groupby(['phase', 'year_submitted'], as_index=False).nct_id.count()
      phase_missing_years(df_phase, 'year_submitted', 'phase', 'nct_id')

      # Data to JSON
      # df_timeline = json.loads(df_year.to_json(orient='records'))
      # df_phase_json = json.loads(df.to_json(orient='records'))


      return render_template("result.html", 
         search = search, 
         number = number_results,
         source_number = source_number,
         timeline = df_year_final.to_json(),
         phase = df_phase_final.to_json())

   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()

