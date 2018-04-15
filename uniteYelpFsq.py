# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:23:31 2018

@author: Maria
"""

import pandas as pd
import os

root = 'D:\Cursuri Master\Knowledge Representation on the Web\Yelp'
dfYelp = pd.read_json(os.path.join(root,'venuesYelp.json'))
dfYelp['Latitude']=[float("{0:.5f}".format(dfYelp['Latitude'][i])) for i in range(0,len(dfYelp))]
dfYelp['Longitude']=[float("{0:.5f}".format(dfYelp['Longitude'][i])) for i in range(0,len(dfYelp))]

root = 'D:\Cursuri Master\Knowledge Representation on the Web\FSQ'
dfFsq = pd.read_json(os.path.join(root,'venuesFSQ.json'))
dfFsq['Latitude']=[float("{0:.5f}".format(dfFsq['Latitude'][i])) for i in range(0,len(dfFsq))]
dfFsq['Longitude']=[float("{0:.5f}".format(dfFsq['Longitude'][i])) for i in range(0,len(dfFsq))]

uniteYelpFsq = pd.merge(dfYelp, dfFsq, on = ['Latitude', 'Longitude'], how = 'outer')

root = 'D:\Cursuri Master\Knowledge Representation on the Web'
dfTripAdv = pd.read_csv(os.path.join(root,'tripadvisor_in-restaurant_sample.csv'))
dfTripAdv['Latitude']=[float("{0:.5f}".format(dfTripAdv['Latitude'][i])) for i in range(0,len(dfTripAdv))]
dfTripAdv['Longitude']=[float("{0:.5f}".format(dfTripAdv['Longitude'][i])) for i in range(0,len(dfTripAdv))]


uniteYelpFsqTrip = pd.merge(dfTripAdv,uniteYelpFsq, on = ['Latitude', 'Longitude'], how = 'outer')