#  FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
# To React: https://realpython.com/the-ultimate-flask-front-end/
#
#Configuration
#

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
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


# Search

@app.route('/', methods = ['GET', 'POST'])
def search():
   if request.method == 'POST':
      search = request.form

      #Connect to db
      conn = sqlite3.connect(DATABASE)

      # Search query
      result_value = request.form['Search']
      first_sql = "SELECT * from all_trials WHERE all_text LIKE "
      term = "'%" + str(result_value) + "%'"
      full_query_string = first_sql + term

      # Query db
      df = pd.read_sql_query(full_query_string, conn)

      # Store data
      number_results = len(df)
      df_year = df.groupby(['year_submitted', 'phase']).nct_id.count()

      return jsonify({'df_year' : df_year.to_json()}, {'number_results' : number_results})

   else:
      return render_template('index.html', data = None)



if __name__ == "__main__": app.run()

