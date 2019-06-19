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


# Views

# Index
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
   return render_template('index.html')

# Results
@app.route('/result', methods = ['GET', 'POST'])
def search():
   if request.method == 'POST':
      search = request.form

      #Connect to db
      conn = sqlite3.connect(DATABASE)

      # Search for string match
      result_value = request.form['Search']
      first_sql = "SELECT * from all_trials WHERE all_text LIKE "
      term = "'%" + str(result_value) + "%'"
      full_query_string = first_sql + term

      # Query db and store results
      df = pd.read_sql_query(full_query_string, conn)
      # Data
      number_results = len(df)
      # Group by year
      df_year = df.groupby(['year_submitted', 'phase']).nct_id.count()

      # all_data = {'data': 'df', 'search': 'search', 'number': 'number_results', 'timeline_graph': 'df_year'}

      return render_template("result.html", 
         data = df, 
         search = search, 
         number = number_results,
         timeline_graph = df_year.to_json())

   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()