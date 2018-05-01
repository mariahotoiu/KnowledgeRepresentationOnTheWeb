# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 11:08:48 2018

@author: Maria
"""
import json
import os
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF


def YELP_RDF(row_size):
	root = 'D:\Cursuri Master\Knowledge Representation on the Web\Yelp'

	root = "json"

	dfYelp = pd.read_json(os.path.join(root,'venuesYelp.json'))

	# create an RDF graph
	g = Graph()

	YELP = Namespace("http://yelp.com/")

	g.bind('yelp',YELP)

	for index, row in dfYelp.head(row_size).iterrows():

		venue_URI = YELP[row['BusinessIdYelp']]

		print "Created {}".format(venue_URI)

		# Every result we get is of type 'YELP:Movie'
		g.add((venue_URI, RDF.type, YELP['venue']))


		g.add((venue_URI, YELP['name'], Literal(row['Name'], lang='en')))



		categories = [a.strip() for a in row['CategoriesYelp'].split(',')]


		for category in categories:
		    g.add((venue_URI, YELP['categoryYelp'], Literal(category)))
		    

		g.add((venue_URI, YELP['city'], Literal(row['City'], lang='en')))


		g.add((venue_URI, YELP['ratingYelp'], Literal(row['RatingYelp'], datatype=XSD.float)))


		g.add((venue_URI, YELP['state'], Literal(row['State'])))
		    

		g.add((venue_URI, YELP['address'], Literal(row['Address'],lang='en')))
		    

		g.add((venue_URI, YELP['reviewCountYelp'], Literal(row['ReviewCountYelp'],datatype = XSD.float)))
		    

		g.add((venue_URI, YELP['postalCode'], Literal(row['PostalCode'])))


		g.add((venue_URI, YELP['latitude'], Literal(row['Latitude'], datatype=XSD.double)))


		g.add((venue_URI, YELP['longitude'], Literal(row['Longitude'], datatype=XSD.double)))

	return g
