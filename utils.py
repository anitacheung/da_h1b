#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""utils.py

Pulls data from from U.S. Department of Labor

__author__ = Anita Cheung
__copyright__ = Copyright 2021
__version__ = 1.0
__maintainer__ = Anita Cheung
__status__ = Dev
"""

import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

URL = "https://www.dol.gov/agencies/eta/foreign-labor/performance"

def get_links(criteria=['H-1B']):
    """Iterates through all links of the page"""
    links = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("a")
    for result in results:
        link = result.get('href')
        if link is None:
            continue
        elif ".xlsx" in link:
            i = 0
            while i < len(criteria):
                if criteria[i] in link:
                    links.append(link)
                    break
                i += 1
    return links

def get_criteria(criteria):
    """Retrieves files data where file names contain the criteria substring"""
    if isinstance(criteria, str):
        criteria = [criteria]
    links = get_links(criteria)

    for link in links:
        filename = link.split('/')[-1]
        filename = os.path.dirname(os.path.realpath(__file__) + '/Data/' + filename)
        print(filename)
        if os.path.isfile(filename):
            #print(filename)
            pass
        else:
            print(filename)
            pass
            #df = pd.read_excel("https://www.dol.gov" + link)
            #df.to_excel(filename)

def merge():
    pathname = os.path.dirname(os.path.realpath(__file__))
    data_pathname = pathname + '/Data'
    dfs = pd.DataFrame()
    for item in os.scandir(data_pathname):
        if dfs.empty:
            dfs = pd.read_excel(item)
        else:
            df = pd.read_excel(item)
            dfs = pd.concat([dfs, df], axis=0, ignore_index=True)
    
    dfs.to_csv(pathname + '/total_data.csv')

def main():
    """Main function"""
    get_criteria(['H-1B', 'LCA'])
    merge()

if __name__ == '__main__':
    main()