# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:40:13 2018

@author: Maria
"""

import pandas as pd
import os


root = 'D:\Cursuri Master\Knowledge Representation on the Web'

X = pd.read_csv(os.path.join(root,'checkins.txt'), sep="\t", header=None)
X.columns = ['UserIdFSQ','BusinessIdFSQ', 'Time', 'Offset']

venues = pd.read_csv(os.path.join(root,'venues.txt'), sep="\t", header=None)
venues.columns = ['BusinessIdFSQ', 'Latitude', 'Longitude', 'CategoryFSQ', 'Country']
   
venuesUS = venues[venues['Country'] == 'US']
venuesCA = venues[venues['Country'] == 'CA']
venuesDE = venues[venues['Country'] == 'DE']
venuesGB = venues[venues['Country'] == 'GB']

venuesArr = [venuesUS, venuesDE, venuesGB, venuesCA]
venues = pd.concat(venuesArr)

result = pd.merge(X, venues, how = 'right', on = 'BusinessIdFSQ')

resultUS = result[result['Country'] == 'US']
resultGB = result[result['Country'] == 'GB']
resultDE = result[result['Country'] == 'DE']
resultCA = result[result['Country'] == 'CA']

resultArr = [resultUS, resultCA, resultDE, resultGB]
result = pd.concat(resultArr)



root = 'D:\Cursuri Master\Knowledge Representation on the Web\FSQ'
out = result.to_json(orient='records')
with open(os.path.join(root,'checkinFSQ.json'), 'w') as f:
    f.write(out)
    
out = venues.to_json(orient='records')
with open(os.path.join(root,'venuesFSQ.json'), 'w') as f:
    f.write(out)


#with open('fsq_reviews.json', 'w') as f:
#    f.write(X.to_json(orient='records', lines=True))