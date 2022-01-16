#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""analysis.py

Analyzes labor data

__author__ = Anita Cheung
__copyright__ = Copyright 2021
__version__ = 1.0
__maintainer__ = Anita Cheung
__status__ = Dev
"""

import pandas as pd
import numpy as np
import datetime as date
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import us
import addfips

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from tableausdk import *
from tableausdk.HyperExtract import *
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

app = dash.Dash(__name__)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

foldername = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(foldername + '/Data/LCA_Disclosure_Data_FY2021_Q4.csv')
df['WAGE_RATE_OF_PAY_TO'].fillna(df['WAGE_RATE_OF_PAY_FROM'], inplace=True)
wage_columns = ['WAGE_RATE_OF_PAY_TO', 'WAGE_RATE_OF_PAY_FROM', 'PREVAILING_WAGE']
for col in wage_columns:
    df[col] = df[col].str.replace('$','')
    df[col] = df[col].str.replace(',','')
    df[col] = df[col].str.replace(' ','')
    df[col] = df[col].astype('float')

df['Wage'] = (df['WAGE_RATE_OF_PAY_TO'] + df['WAGE_RATE_OF_PAY_FROM'])/2

df['JOB_TITLE'] = df['JOB_TITLE'].str.replace('\t','')
df['JOB_TITLE'] = df['JOB_TITLE'].str.strip()
df['JOB_TITLE'] = df['JOB_TITLE'].str.lower()

# Data Cleaning
num_na = df['JOB_TITLE'].isna().sum()
jobs = df['JOB_TITLE'].value_counts().rename('Count')

# Create n-grams
def generate_N_grams(text,ngram=2):
  words=[word for word in text.split(" ") if word not in set(stopwords.words('english'))]
  temp=zip(*[words[i:] for i in range(0,ngram)])
  ans=[' '.join(ngram) for ngram in temp]
  return ans

# Summary
wage_column = 'PREVAILING_WAGE'
df = df[df['WORKSITE_STATE']=='NY']
mean_salary = df.groupby(['JOB_TITLE'], as_index=True).agg({wage_column:'mean'})
mean_salary = mean_salary.join(jobs)
mean_salary = mean_salary.sort_values(wage_column, ascending=False)
print(mean_salary)









plotme = False
if plotme:
    # Duration
    df['RECEIVED_DATE'] = pd.to_datetime(df['RECEIVED_DATE'], errors='coerce')
    df['DECISION_DATE'] = pd.to_datetime(df['DECISION_DATE'], errors='coerce')
    df['Duration (Days)'] = (df['DECISION_DATE'] - df['RECEIVED_DATE']) /np.timedelta64(1, 'D')
    df = df[(df['CASE_STATUS']!='Certified - Withdrawn') & (df['CASE_STATUS']!='Withdrawn')]    
    duration = px.histogram(df, x='Duration (Days)', color='CASE_STATUS', opacity=0.8)

    # Percent of Case Status
    case_status = px.bar(df, x='CASE_STATUS', color='VISA_CLASS')

    # Salary
    df['WAGE_RATE_OF_PAY_TO'].fillna(df['WAGE_RATE_OF_PAY_FROM'], inplace=True)
    df['WAGE_RATE_OF_PAY_TO'] = df['WAGE_RATE_OF_PAY_TO'].str.replace('$','')
    df['WAGE_RATE_OF_PAY_TO'] = df['WAGE_RATE_OF_PAY_TO'].str.replace(',','')
    df['WAGE_RATE_OF_PAY_TO'] = df['WAGE_RATE_OF_PAY_TO'].str.replace(' ', '')

    df['WAGE_RATE_OF_PAY_FROM'] = df['WAGE_RATE_OF_PAY_FROM'].str.replace('$','')
    df['WAGE_RATE_OF_PAY_FROM'] = df['WAGE_RATE_OF_PAY_FROM'].str.replace(',','')
    df['WAGE_RATE_OF_PAY_FROM'] = df['WAGE_RATE_OF_PAY_FROM'].str.replace(' ','')

    df['Wage'] = (df['WAGE_RATE_OF_PAY_TO'].astype('float') + df['WAGE_RATE_OF_PAY_FROM'].astype('float'))/2
    #df[df['WAGE_UNIT_OF_PAY']=='Hour']['Wage'] = df[df['WAGE_UNIT_OF_PAY']=='Hour']['Wage'] * 2080
    wage = px.histogram(df, x='Wage')

    # Location
    fips = us.states.mapping('abbr', 'fips')
    df['Fips'] = df['WORKSITE_STATE'].apply(lambda x: fips[x] + '000')
    location = px.choropleth(df,
            locations = 'WORKSITE_STATE',
            color='Wage',
            hover_name='WORKSITE_STATE',
            locationmode='USA-states',
            color_continuous_scale='spectral_r',
            scope='usa'
            )


    # Plot
    app.layout = html.Div(children=[
        html.H1(children='H1B Data'),

        html.Div(children='''
            Location
        '''),

        dcc.Graph(
            id='location-graph',
            figure=location
        ),

        html.Div(children='''
            Duration to Resolution
        '''),

        dcc.Graph(
            id='duration-graph',
            figure=duration
        ),

        html.Div(children='''
            Case Status by Visa Class
        '''),

        dcc.Graph(
            id='case-status-graph',
            figure=case_status
        ),

        html.Div(children='''
            Annual Salary
        '''),

        dcc.Graph(
            id='salary-graph',
            figure=wage
        )
    ])

if __name__ == '__main__':
    if plotme:
        app.run_server(debug=True)
