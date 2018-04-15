# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 10:42:25 2018

@author: Maria
"""

import json
import os
import pandas as pd

def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob

root = 'D:\Cursuri Master\Knowledge Representation on the Web\Yelp'
df = pd.DataFrame([convert(line) for line in file(os.path.join(root,'business.json'))])
df.drop(columns=['neighborhood'])
dfNew = pd.DataFrame()
dfNew['BusinessIdYelp'] = df['business_id']
dfNew['Name'] = df['name']
dfNew['Address'] = df['address']
dfNew['City'] = df['city']
dfNew['State'] =df['state']
dfNew['PostalCode'] = df['postal_code']
dfNew['Latitude'] = df['latitude']
dfNew['Longitude'] =  df['longitude']
dfNew['RatingYelp'] = df['stars']
dfNew['ReviewCountYelp'] = df['review_count']
dfNew['CategoriesYelp'] = df['categories']
dfNew['Latitude']=[float("{0:.6f}".format(dfNew['Latitude'][i])) for i in range(0,len(dfNew))]
dfNew['Longitude']=[float("{0:.6f}".format(dfNew['Longitude'][i])) for i in range(0,len(dfNew))]

out = dfNew.to_json(orient='records')
with open(os.path.join(root,'venuesYelp.json'), 'w') as f:
    f.write(out)
