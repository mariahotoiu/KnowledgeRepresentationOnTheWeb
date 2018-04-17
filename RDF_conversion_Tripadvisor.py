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

def TripAdv_RDF(row_size):

	# create an RDF graph
	TripAdv_graph = Graph()

	dfTripAdv = pd.read_csv('tripadvisor_in-restaurant_sample.csv')

	TripAdv = Namespace("http://TripAdv.com/")

	TripAdv_graph.bind("TripAdv",TripAdv)

	root = 'json/'

	# Build dataframe Yelp
	# dfYelp = pd.read_json(root+'venuesYelp.json')
	# dfYelp['Latitude']=[float("{0:.5f}".format(dfYelp['Latitude'][i])) for i in range(0,len(dfYelp))]
	# dfYelp['Longitude']=[float("{0:.5f}".format(dfYelp['Longitude'][i])) for i in range(0,len(dfYelp))]


	# for elem in venueIDs:
	for index, row in dfTripAdv.head(row_size).iterrows():
		# response = requests.get(foursquare_api_link+elem,params=params).json()


		venueID = TripAdv[row["Restaurant ID"]]

		print("Created {}".format(venueID))

		TripAdv_graph.add((venueID, RDF.type, TripAdv['venueID']))
		TripAdv_graph.add((venueID, TripAdv['name'], Literal(row["Name"], lang='en')))
		TripAdv_graph.add((venueID, TripAdv['city'], Literal(row["City"], lang='en')))
		TripAdv_graph.add((venueID, TripAdv['state'], Literal(row["State"], lang='en')))
		TripAdv_graph.add((venueID, TripAdv['rating'], Literal(row["Rating"], datatype = XSD.integer)))

		TripAdv_graph.add((venueID, TripAdv['longitude'], Literal(float("{0:.5f}".format(row["Longitude"])), datatype=XSD.double)))
		TripAdv_graph.add((venueID, TripAdv['latitude'], Literal(float("{0:.5f}".format(row["Latitude"])), datatype=XSD.double)))


		# Build up adress Checking for the right lines. Some adresses are worse so can not be checked very well.
		# So a NaN value is added to that value

		if not(isinstance(row["Address"],float)):
			list_location = row["Address"].split(',')
			if len(list_location) == 4:
				street, postalcode, state, country = list_location
			elif len(list_location) == 3:
				street, postalcode, state = list_location
			elif len(list_location) == 2:
				street, postalcode = list_location
			elif len(list_location) > 4:
				street = list_location[0] + list_location[1]
				postalcode = list_location[2]
			else:
				street = row["Address"]
				postalcode = row["Address"]

		else:
			street = row["Address"]
			postalcode = row["Address"]

		TripAdv_graph.add((venueID, TripAdv['address'], Literal(street, lang='en')))
		TripAdv_graph.add((venueID, TripAdv['postalcode'], Literal(postalcode, lang='en')))
		TripAdv_graph.add((venueID, TripAdv['country'], Literal(row["Country"], lang='en')))


		if isinstance(row['Cuisine'],float):
			TripAdv_graph.add((venueID, TripAdv['CuisineType'], Literal(row['Cuisine'], lang='en')))
		else:
			for category in row['Cuisine'].split(','):
				TripAdv_graph.add((venueID, TripAdv['CuisineType'], Literal(category, lang='en')))
		
		TripAdv_graph.add((venueID, TripAdv['reviewcount'], Literal(row["Total Review"],datatype = XSD.integer)))


	return TripAdv_graph 