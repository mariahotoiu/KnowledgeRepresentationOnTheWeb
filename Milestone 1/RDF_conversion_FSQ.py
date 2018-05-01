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

def RDF_FSQ(row_size, call_api=False):

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

	# Build dataframe FSQ Reviews

	# Build dataframe Fsq
	dfFsq['Latitude']=[float("{0:.5f}".format(dfFsq['Latitude'][i])) for i in range(0,len(dfFsq))]
	dfFsq['Longitude']=[float("{0:.5f}".format(dfFsq['Longitude'][i])) for i in range(0,len(dfFsq))]

	if row_size > len(dfFsq.index)  or row_size == 0:
		row_size = len(dfFsq.index)

	venue_val = 0

	# for elem in venueIDs:
	for index, row in dfFsq.head(row_size).iterrows():
		if call_api:
			response = requests.get(foursquare_api_link+row["BusinessIdFSQ"],params=params).json()
			# response = requests.get(foursquare_api_link+elem,params=params).json()
			json_check = json_normalize(response)
			# print(json_check.columns.values.tolist())


			venueID = foursquare[row["BusinessIdFSQ"]]

			print("Created {}".format(venueID))

			foursquare_graph.add((venueID, RDF.type, foursquare['venueID']))
			foursquare_graph.add((venueID, foursquare['name'], Literal(json_check['response.venue.name'].iloc[0], lang='en')))
			foursquare_graph.add((venueID, foursquare['city'], Literal(json_check['response.venue.location.city'].iloc[0], lang='en')))
			foursquare_graph.add((venueID, foursquare['state'], Literal(json_check['response.venue.location.state'].iloc[0], lang='en')))
			foursquare_graph.add((venueID, foursquare['longitude'], Literal(float("{0:.5f}".format(json_check['response.venue.location.lng'].iloc[0])), datatype=XSD.double)))
			foursquare_graph.add((venueID, foursquare['latitude'], Literal(float("{0:.5f}".format(json_check['response.venue.location.lat'].iloc[0])), datatype=XSD.double)))
			# Build up adress
			street, postalcode, country = json_check['response.venue.location.formattedAddress'].iloc[0]

			foursquare_graph.add((venueID, foursquare['address'], Literal(street, lang='en')))
			foursquare_graph.add((venueID, foursquare['postalcode'], Literal(postalcode, lang='en')))
			foursquare_graph.add((venueID, foursquare['country'], Literal(country, lang='en')))

			for category in json_check['response.venue.categories'].iloc[0]:
				foursquare_graph.add((venueID, foursquare['categoryFSQ'], Literal(category["name"], lang='en')))
			
			foursquare_graph.add((venueID, foursquare['checkinsCountFSQ'], Literal(json_check['response.venue.stats.checkinsCount'].iloc[0],datatype = XSD.float)))
		else:
			if not(venue_val == row["BusinessIdFSQ"]):
				venue_val = row["BusinessIdFSQ"]
				venueID = foursquare[venue_val]

				# print("Created {}".format(venueID))

				foursquare_graph.add((venueID, RDF.type, foursquare['venueID']))			
				foursquare_graph.add((venueID, foursquare['longitude'], Literal(row['Longitude'], datatype=XSD.double)))
				foursquare_graph.add((venueID, foursquare['latitude'], Literal(row['Longitude'], datatype=XSD.double)))





	# Build dataframe FSQ Checkins

	# Build dataframe Fsq
	map_checkin_FSQ = "json/checkinsFSQ.json"
	dfFsq_checkin = pd.read_json(map_checkin_FSQ)

	if row_size > len(dfFsq_checkin.index) or row_size == 0:
		row_size = len(dfFsq_checkin.index)

	# for elem in venueIDs:
	for index, row in dfFsq_checkin.head(row_size).iterrows():



		UserIdFSQ = foursquare[row["UserIdFSQ"]]
		foursquare_graph.add((UserIdFSQ, RDF.type, foursquare['UserIdFSQ']))


		venueID = foursquare[row["BusinessIdFSQ"]]

		foursquare_graph.add((UserIdFSQ, foursquare['checkin'], venueID))

		foursquare_graph.add((UserIdFSQ, foursquare['checkintime'], Literal(row["Time"], lang='en') ))



	return foursquare_graph


