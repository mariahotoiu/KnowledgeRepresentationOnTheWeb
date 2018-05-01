# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:23:31 2018

@author: Maria
"""

import pandas as pd
import os
import json
import requests
from pandas.io.json import json_normalize

root = 'Yelp'
dfYelp = pd.read_json(os.path.join(root,'venuesYelp.json'))
dfYelp['Latitude']=[float("{0:.6f}".format(dfYelp['Latitude'][i])) for i in range(0,len(dfYelp))]
dfYelp['Longitude']=[float("{0:.6f}".format(dfYelp['Longitude'][i])) for i in range(0,len(dfYelp))]

root = 'D:\Cursuri Master\Knowledge Representation on the Web\FSQ'
dfFsq = pd.read_json(os.path.join(root,'venuesFSQ.json'))
dfFsq['Latitude']=[float("{0:.6f}".format(dfFsq['Latitude'][i])) for i in range(0,len(dfFsq))]
dfFsq['Longitude']=[float("{0:.6f}".format(dfFsq['Longitude'][i])) for i in range(0,len(dfFsq))]

uniteYelpFsq = pd.merge(dfYelp, dfFsq, on = ['Latitude', 'Longitude'], how = 'outer')
uniteYelpFsq = uniteYelpFsq.dropna(axis=0, how = 'any')
print(uniteYelpFsq)

foursquare_api_link = "https://api.foursquare.com/v2/venues/"
params = dict(client_id="",
	  client_secret="",
	  v="",
	  limit=1)

uniteYelpFsq['RatingFsq'] = ""
uniteYelpFsq['Fsq URL'] = ""

for index, row in uniteYelpFsq.iterrows():
    response = requests.get(foursquare_api_link+row["BusinessIdFSQ"],params=params).json()
    # response = requests.get(foursquare_api_link+elem,params=params).json()
    json_check = json_normalize(response)
    try:
        uniteYelpFsq['RatingFsq'][index] = json_check['response.venue.rating'].iloc[0]
    except KeyError:
        pass
    uniteYelpFsq['Fsq URL'][index] = json_check['response.venue.canonicalUrl'].iloc[0] 

out = uniteYelpFsq.to_json(orient='records')[1:-1]
root = 'json'
with open(os.path.join(root,'fsqYelp.json'), 'w') as f:
    f.write(out)
    
           

