# FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run

#
#Configuration
#

from flask import Flask, render_template
import sqlite3
import pandas as pd

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



if __name__ == "__main__": app.run()


