# FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run

#
#Configuration
#

from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE = '../data/working_data/database.db'


# 
#Views
#

@app.route('/')
@app.route('/index')
def index():
	conn = sqlite3.connect(DATABASE)
	df = pd.read_sql_query("SELECT * FROM all_trials LIMIT 1", conn)
	return render_template('index.html', data = df.to_html())

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form

      # conn = sqlite3.connect(DATABASE)

      # first_sql = 'SELECT * FROM all_trials WHERE all_text LIKE '
      # result_value = request.form['Search']
      # query_string =   first_sql + str(result_value) + ' LIMIT 1'

      # df = pd.read_sql_query(query_string, conn)

      return render_template("result.html",result = result)

if __name__ == "__main__": app.run()


