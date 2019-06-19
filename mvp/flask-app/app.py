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

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE = '../data/working_data/database.db'

#Views

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
   return render_template('index.html')


@app.route('/result', methods = ['GET', 'POST'])
def search():
   if request.method == 'POST':
      search = request.form

      conn = sqlite3.connect(DATABASE)

      # Get result and search for string match
      # ie: # '%breast cancer%';
      result_value = request.form['Search']
      first_sql = "SELECT * from all_trials WHERE all_text LIKE "
      term = "'%" + str(result_value) + "%'"
      query_string = first_sql + term

      # Query db and store results in df
      df = pd.read_sql_query(query_string, conn)
      number_results = len(df)
      df_head = df.head()

      # return jsonify({'data' : df.to_json()})

      return render_template("result.html", 
      	data = df, 
      	result = search, 
      	number = number_results)

   else:
      return render_template('index.html', data = None)


if __name__ == "__main__": app.run()

