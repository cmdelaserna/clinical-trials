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

DATABASE = '../data/working_data/working-database.db'

'''
FUNCTIONS
'''

# Query
def build_query(search_field):
   # Global variables
   global search, full_query
   search = request.form   

   # Build query
   result_value = request.form[search_field]
   query = "SELECT * from all_trials WHERE all_text LIKE "
   term = "'%" + str(result_value) + "%'"

   full_query = query + term

   return full_query

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
      df = pd.read_sql_query(full_query, conn)
      number_results = len(df)

      # Get number of sources in query
      df_source = df.groupby(['source'], as_index=False).nct_id.count()
      source_number = df_source['source'].nunique()

      #
      # TIMELINE: Group by year, add missing years
      #

      df_year = df.groupby(['year_submitted'], as_index=False).nct_id.count()

      # Create df with missing years, zeros
      columns = ['year_submitted', 'nct_id']
      all_years = np.arange(1999, 2020)

      missing_years = np.setdiff1d(all_years, pd.Series(df_year['year_submitted']))
      zeros = ([0] * len(missing_years))
      
      zippedList =  list(zip(missing_years, zeros))
      df_all_years = pd.DataFrame(zippedList, columns = columns)

      # Fill missing years in timeline df
      df_concat = pd.concat([df_all_years, df_year], ignore_index=True)
      df_timeline = df_concat.sort_values(['year_submitted'])
      df_timeline = df_timeline.set_index('year_submitted')
      
      ############
      ###

      #
      # Trials by phase: groupby, add missing columns, fixed order
      #
      df_phase = df.groupby(['phase'], as_index=False).nct_id.count()
      
      df_phase = df_phase.set_index('phase')


      # Pass data to front-end
      return render_template("result.html", 
         search = search, 
         number = number_results,
         source_number = source_number,
         timeline = df_timeline.to_json(),
         phase = df_phase.to_json())

   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()

