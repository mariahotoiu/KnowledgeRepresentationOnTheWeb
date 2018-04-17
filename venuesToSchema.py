# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:33:19 2018

@author: Maria
"""
import json
import os
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF, BNode


root = 'D:\Cursuri Master\Knowledge Representation on the Web\Yelp'
with open(os.path.join(root,'venuesYelp.json')) as json_data:
    response = json.load(json_data)

# create an RDF graph
g = Graph()

venue = BNode()

schema = Namespace("http://schema.org/")

g.bind('schema',schema)


g.add((venue, RDF.type, schema.localBusiness))


g.add((venue, schema.name, Literal(response[1]['Name'], lang='en')))



#categories = [a.strip() for a in response[1]['CategoriesYelp'].split(',')]
#
#
#for category in categories:
#    g.add((venue_URI, ['categoryYelp'], Literal(category)))

address = BNode() 
g.add((venue, schema.address, address ))
g.add((address, RDF.type, schema.PostalAddress))
g.add((address, schema.addressLocalitly, Literal(response[1]['City'], lang='en')))
g.add((address, schema.streetAddress,Literal(response[1]['Address'],lang='en')))
g.add((address, schema.postalCode, Literal(response[1]['PostalCode'])))
g.add((address, schema.addressRegion, Literal(response[1]['State'])))
geo = BNode()
g.add((venue,schema.geo,geo))
g.add((geo, RDF.type, schema.GeoCoordinates))
g.add((geo,schema.latitude,Literal(response[1]['Latitude'], datatype=XSD.decimal)))
g.add((geo,schema.longitude,Literal(response[1]['Longitude'], datatype=XSD.decimal)))
rating = BNode()
g.add((venue, schema.aggregateRating, rating))
g.add((rating, RDF.type, schema.aggregateRating))
g.add((rating, schema.ratingValue,Literal(response[1]['RatingYelp'], datatype=XSD.decimal)))
g.add((rating, schema.reviewCount, Literal(response[1]['ReviewCountYelp'],datatype = XSD.integer)))
g.add((rating, schema.author, Literal('Yelp')))

print g.serialize(format='turtle')

