from flask import Flask, render_template, request
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
import json
import numpy as np

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
# def add_missing_years(data, column_year, column_name_count):

#    global df_year_final

#    all_years = np.arange(1999, 2020)
#    missing_years = [item for item in all_years if item not in data]
#    zeros = ([0] * len(missing_years))

#    columns = [column_year, column_name_count] #ie, ['year_submitted', 'nct_id']

#    zippedList =  list(zip(missing_years, zeros))
#    df_all_years = pd.DataFrame(zippedList, columns = columns) 

#    df_year_final = pd.concat([data, df_all_years], ignore_index=True)
#    df_year_final = df_year_final.sort_values(by=column_year).reset_index(drop=True)

#    return df_year_final

def add_missing_years(data, column_year, column_name_count):

   global df_year_final

   all_years = np.arange(1999, 2020)
   missing_years = [item for item in all_years if item not in data]
   zeros = ([0] * len(missing_years))

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