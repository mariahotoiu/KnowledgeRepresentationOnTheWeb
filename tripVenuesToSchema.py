# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 15:46:05 2018

@author: Maria
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 00:42 2018
@author: Thomas
"""
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF, BNode
#import requests
#import json
import pandas as pd
import os
#from pandas.io.json import json_normalize


# create an RDF graph
TripAdv_graph = Graph()
root = 'D:\Cursuri Master\Knowledge Representation on the Web\Trpadvisor'
dfTripAdv = pd.read_csv(os.path.join(root,'tripadvisor_in-restaurant_sample.csv'))

schema = Namespace("http://schema.org/")

TripAdv_graph.bind("schema",schema)

root = 'json/'

# Build dataframe Yelp
# dfYelp = pd.read_json(root+'venuesYelp.json')
# dfYelp['Latitude']=[float("{0:.5f}".format(dfYelp['Latitude'][i])) for i in range(0,len(dfYelp))]
# dfYelp['Longitude']=[float("{0:.5f}".format(dfYelp['Longitude'][i])) for i in range(0,len(dfYelp))]


# for elem in venueIDs:
for index, row in dfTripAdv.head(5).iterrows():
    venue = BNode()
	
    TripAdv_graph.add((venue, RDF.type, schema.Restaurant))
    TripAdv_graph.add((venue, schema['name'], Literal(row["Name"], lang='en')))
    geo = BNode()
    TripAdv_graph.add((venue,schema.geo,geo))
    TripAdv_graph.add((geo, RDF.type, schema.GeoCoordinates))
    TripAdv_graph.add((geo,schema.latitude,Literal(row['Latitude'], datatype=XSD.decimal)))
    TripAdv_graph.add((geo,schema.longitude,Literal(row['Longitude'], datatype=XSD.decimal)))
       
    rating = BNode()
    TripAdv_graph.add((venue, schema.aggregateRating, rating))
    TripAdv_graph.add((rating, RDF.type, schema.AggregateRating))
    TripAdv_graph.add((rating, schema.ratingValue,Literal(row['Rating'], datatype=XSD.decimal)))
    TripAdv_graph.add((rating, schema.author, Literal('TripAdvisor')))
    TripAdv_graph.add((rating, schema.reviewCount, Literal(row["Total Review"], datatype = XSD.integer)))

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
    address = BNode() 
    TripAdv_graph.add((venue, schema.address, address ))
    TripAdv_graph.add((address, RDF.type, schema.PostalAddress))   
    TripAdv_graph.add((address, schema.streetAddress, Literal(street, lang='en')))
    TripAdv_graph.add((address, schema.postalCode, Literal(postalcode, lang='en')))
    TripAdv_graph.add((address, schema.addressLocality, Literal(row["City"]+', '+row["Country"], lang='en')))
    TripAdv_graph.add((address, schema.addressRegion, Literal(row["State"], lang='en')))

    if not isinstance(row['Cuisine'],float):
		for category in row['Cuisine'].split(','):
			TripAdv_graph.add((venue, schema.servesCuisine, Literal(category, lang='en')))
    identifier = BNode()
    TripAdv_graph.add((venue, schema.identifier, identifier))
    TripAdv_graph.add((identifier, RDF.type, schema.PropertyValue))
    TripAdv_graph.add((identifier, schema.propertyID, Literal('BusinessIdTripAdvisor')))
    TripAdv_graph.add((identifier, schema.value,Literal(row['Uniq Id'])))
   
print(TripAdv_graph.serialize(format='turtle'))
