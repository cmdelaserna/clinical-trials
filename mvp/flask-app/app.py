   # FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
# To React: https://realpython.com/the-ultimate-flask-front-end/
#
#Configuration
#

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from sqlalchemy import create_engine
import pandas as pd
import json
import numpy as np
# import sqlite3


'''
CONFIGURATION
'''
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'key'

# app.config['WHOOSH_BASE'] = '../data/whooshBase.db'

#sqlite
# DATABASE = '../data/working_data/working-database.db'

#postgres
host = 'postgresql://cms@localhost:5432/'
db = 'aact'
connection = host + db
engine = create_engine(connection)



'''
FUNCTIONS & CLASSES
'''

# Query
def build_query(search_field):
   # Global variables
   global search, full_query, df

   # Create a df with search_terms table
   table_name = 'search_terms'
   search_table = "SELECT * FROM " + table_name
   partial_query = pd.read_sql_query(search_table, con = engine)

   # Look for search value in table
   search = request.form

   result_value = request.form[search_field].lower()

   try:
      table_value = partial_query[partial_query['search_term'].str.match(result_value)]
      table_value = table_value.return_table.values[0]
      # Final query
      full_query = "SELECT * FROM " + table_value
      df = pd.read_sql_query(full_query, con = engine)

      return search, full_query, df
   
   except:
      empty_query = "SELECT * FROM celiac limit 0"
      df = pd.read_sql_query(empty_query, con = engine)

      return search, full_query, df



# Process search results
def process_result(source = 'source', date = 'year_posted', recruiting = 'recruiting_status'):
      global number_results, source_number, df_timeline, df_phase

      number_results = len(df)

      df_source = df.groupby([source], as_index=False).nct_id.count()
      source_number = df_source[source].nunique()

      #
      # TIMELINE: Group by year, add missing years
      df_year = df.groupby([date], as_index=False).agg({'nct_id':'count', recruiting:'sum'})

      # Create df with missing years, zeros
      columns = [date, 'nct_id']
      all_years = np.arange(1999, 2020)
      missing_years = np.setdiff1d(all_years, pd.Series(df_year[date]))
      zeros = ([0] * len(missing_years))
      zippedList =  list(zip(missing_years, zeros))
      df_all_years = pd.DataFrame(zippedList, columns = columns)

      # Fill missing years in timeline df
      df_concat = pd.concat([df_all_years, df_year], ignore_index=True, sort = True)
      df_timeline = df_concat.sort_values([date])
      df_timeline = df_timeline.set_index(date)
      df_timeline.columns = ['All Trials', 'Recruiting']
      df_timeline['Recruiting'].fillna(0, inplace = True)

      # Trials by phase: groupby, add missing columns, fixed order    
      df_phase = df.groupby(['phase'], as_index=False).agg({'nct_id':'count', recruiting:'sum'})
      df_phase = df_phase.set_index('phase')
      df_phase.columns = ['All Trials', 'Recruiting']   

def generate_table(data):
   global table
   
   # Pending: adding url to dataframe
   columns = ['official_title', 'mesh_terms', 'study_first_posted_date', 'recruiting_status']
   table = data[columns].head(11)
   
   return table


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
      build_query('Search')
      process_result()
      generate_table(df)

      return render_template("result.html", 
         data_index = df.to_json(orient = 'index'),
         table = table.to_html(header=False, classes = 'td'),
         search = search, 
         number = number_results,
         source_number = source_number,
         timeline = df_timeline.to_json(),
         phase = df_phase.to_json())

   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()

