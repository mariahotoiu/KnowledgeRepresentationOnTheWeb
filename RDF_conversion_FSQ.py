# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 00:42 2018

@author: Thomas
"""
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF
import requests
import json
import pandas as pd
import os
from pandas.io.json import json_normalize


# create an RDF graph
foursquare_graph = Graph()

foursquare_api_link = "https://api.foursquare.com/v2/venues/"
params = dict(
  client_id="QS20SFPKYDQ5B25XPHE3PI3TKDEQ5KBBBYJBJVOX2B1SGKIR",
  client_secret="3W1AD4PK5W4CON5VVDZTKSPRYJKLWDNZQ01O2CEX0KTDQK5Z",
  v="20180323",
  limit=1)

map_loc_FSQ = "json/venuesFSQ.json"

venueIDs = ["49bbd6c0f964a520f4531fe3", "4ce1863bc4f6a35d8bd2db6c"]

foursquare = Namespace("http://foursquare.com/")

foursquare_graph.bind("foursquare",foursquare)

dfFsq = pd.read_json(map_loc_FSQ)

root = 'json/'

# Build dataframe Yelp
# dfYelp = pd.read_json(root+'venuesYelp.json')
# dfYelp['Latitude']=[float("{0:.5f}".format(dfYelp['Latitude'][i])) for i in range(0,len(dfYelp))]
# dfYelp['Longitude']=[float("{0:.5f}".format(dfYelp['Longitude'][i])) for i in range(0,len(dfYelp))]


# for elem in venueIDs:
for index, row in dfFsq.head(5).iterrows():
	response = requests.get(foursquare_api_link+row["BusinessIdFSQ"],params=params).json()
	# response = requests.get(foursquare_api_link+elem,params=params).json()
	json_check = json_normalize(response)
	# print(json_check.columns.values.tolist())


	venueID = foursquare[row["BusinessIdFSQ"]]

	print("Created {} name: {}".format(venueID, json_check['response.venue.name'].iloc[0]))

	foursquare_graph.add((venueID, RDF.type, foursquare['venueID']))
	foursquare_graph.add((venueID, foursquare['name'], Literal(json_check['response.venue.name'].iloc[0], lang='en')))
	foursquare_graph.add((venueID, foursquare['city'], Literal(json_check['response.venue.location.city'].iloc[0], lang='en')))
	foursquare_graph.add((venueID, foursquare['state'], Literal(json_check['response.venue.location.state'].iloc[0], lang='en')))
	foursquare_graph.add((venueID, foursquare['longitude'], Literal(float("{0:.5f}".format(json_check['response.venue.location.lng'].iloc[0])))))
	foursquare_graph.add((venueID, foursquare['latitude'], Literal(float("{0:.5f}".format(json_check['response.venue.location.lat'].iloc[0])))))
	# Build up adress
	street, postalcode, country = json_check['response.venue.location.formattedAddress'].iloc[0]

	foursquare_graph.add((venueID, foursquare['address'], Literal(street, lang='en')))
	foursquare_graph.add((venueID, foursquare['postalcode'], Literal(postalcode, lang='en')))
	foursquare_graph.add((venueID, foursquare['country'], Literal(country, lang='en')))

	for category in json_check['response.venue.categories'].iloc[0]:
		foursquare_graph.add((venueID, foursquare['categoryFSQ'], Literal(category["name"], lang='en')))
	
	foursquare_graph.add((venueID, foursquare['checkinsCountFSQ'], Literal(json_check['response.venue.stats.checkinsCount'].iloc[0], lang='en')))



print(foursquare_graph.serialize(format='turtle'))




    

    




