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
import yfinance

'''
def assemble_data():
    filename = "LCA_Disclosure_Data_FY2021_Q"
    foldername = os.path.dirname(os.path.realpath(__file__))
    dfs = pd.DataFrame()
    
    for i in range(1,5):
        df = pd.read_excel(foldername + '/Data/' + filename + str(i) + '.xlsx')
        if dfs.empty:
            dfs = df
        else:
            dfs = pd.concat([dfs, df], axis=0, ignore_index=True)
    
    dfs = pd.read_excel(foldername + '/Data/LCA_Disclosure_Data_FY2021_Q4.xlsx')
    dfs.to_csv(foldername + '/total.csv')

def get_data():
    """"""
    pathname = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(pathname + '/total.csv')
    return df

def analysis_duration(df):
    """Time to complete cases"""
    df['RECEIVED_DATE'] = pd.to_datetime(df['RECEIVED_DATE'], errors='coerce')
    df['DECISION_DATE'] = pd.to_datetime(df['DECISION_DATE'], errors='coerce')
    df['Duration'] = (df['DECISION_DATE'] - df['RECEIVED_DATE']) /np.timedelta64(1, 'M')
    df = df[(df['CASE_STATUS']!='Certified - Withdrawn') & (df['CASE_STATUS']!='Withdrawn')]
    app = dash.Dash(__name__)

    fig = px.histogram(df, x='Duration', color='CASE_STATUS', text_auto=True, opacity=0.8)
    app.layout = html.Div(children=[
        html.H1(children="Time to Resolution"),
        html.Div(children=Time to complete case),
        dcc.Graph(
            id='duration-graph',
            figure=fig
        )
    ]
    app.run_server(debug=True)
'''

app = dash.Dash(__name__)

foldername = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(foldername + '/Data/LCA_Disclosure_Data_FY2021_Q4.csv')
df['RECEIVED_DATE'] = pd.to_datetime(df['RECEIVED_DATE'], errors='coerce')
df['DECISION_DATE'] = pd.to_datetime(df['DECISION_DATE'], errors='coerce')
df['Duration'] = (df['DECISION_DATE'] - df['RECEIVED_DATE']) /np.timedelta64(1, 'M')
df = df[(df['CASE_STATUS']!='Certified - Withdrawn') & (df['CASE_STATUS']!='Withdrawn')]    
fig = px.histogram(df, x='Duration', color='CASE_STATUS', text_auto=True, opacity=0.8)
app.layout = html.Div(children=[
    html.H1(children="Time to Resolution"),
    html.Div(children='''Time to complete case'''),
    dcc.Graph(
        id='duration-graph',
        figure=fig
    )
]
app.run_server(debug=True)

if __name__=='__main__':
    app.run_server(debug=True)

'''
def main():
    """Main function"""
    foldername = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(foldername + '/Data/LCA_Disclosure_Data_FY2021_Q4.csv')
    analysis_duration(df)
   
if __name__ == '__main__':
    main()
'''