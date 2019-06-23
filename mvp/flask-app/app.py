# FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
# To React: https://realpython.com/the-ultimate-flask-front-end/
#
#Configuration
#

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
import json
import time

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

      # Get number of sources in query
      df_source = df.groupby(['source'], as_index=False).nct_id.count()
      source_number = df_source['source'].nunique()

      # Trials by phase, year
      df_phase = df.groupby(['phase', 'year_submitted'], as_index=False).nct_id.count()


      return render_template("result.html", 
         search = search, 
         number = number_results,
         df = df.to_json(),
         timeline_graph = df_year.to_json(),
         source_number = source_number,
         phase = df_phase.to_json())


   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()

