# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 11:08:48 2018

@author: Maria
"""
import json
import os
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF

root = 'D:\Cursuri Master\Knowledge Representation on the Web\Yelp'
with open(os.path.join(root,'venuesYelp.json')) as json_data:
    response = json.load(json_data)

# create an RDF graph
g = Graph()

YELP = Namespace("http://yelp.com/")

g.bind('yelp',YELP)

venue_URI = YELP[response[1]['BusinessIdYelp']]

print "Created {}".format(venue_URI)

# Every result we get is of type 'YELP:Movie'
g.add((venue_URI, RDF.type, YELP['venue']))


g.add((venue_URI, YELP['name'], Literal(response[1]['Name'], lang='en')))



categories = [a.strip() for a in response[1]['CategoriesYelp'].split(',')]


for category in categories:
    g.add((venue_URI, YELP['categoryYelp'], Literal(category)))
    

g.add((venue_URI, YELP['city'], Literal(response[1]['City'], lang='en')))


g.add((venue_URI, YELP['ratingYelp'], Literal(response[1]['RatingYelp'], datatype=XSD.double)))


g.add((venue_URI, YELP['state'], Literal(response[1]['State'])))
    

g.add((venue_URI, YELP['address'], Literal(response[1]['Address'],lang='en')))
    

g.add((venue_URI, YELP['reviewCountYelp'], Literal(response[1]['ReviewCountYelp'],datatype = XSD.integer)))
    

g.add((venue_URI, YELP['postalCode'], Literal(response[1]['PostalCode'])))


g.add((venue_URI, YELP['latitude'], Literal(response[1]['Latitude'], datatype=XSD.double)))


g.add((venue_URI, YELP['longitude'], Literal(response[1]['Longitude'], datatype=XSD.double)))
print g.serialize(format='turtle')
