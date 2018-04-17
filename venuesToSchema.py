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

root2 = 'D:\Cursuri Master\Knowledge Representation on the Web'
with open(os.path.join(root2,'schemaTypes.txt'), "r") as word_list:
    schemaTypes = word_list.read().split('\n')

with open(os.path.join(root2,'schemaSubtypes.txt'), "r") as word_list:
    schemaSubTypes = word_list.read().split('\n')


g = Graph()

venue = BNode()

schema = Namespace("http://schema.org/")

g.bind('schema',schema)

categories = [a.strip() for a in response[1]['CategoriesYelp'].split(',')]
#
#
cat = 0
for category in categories:
    category = category.replace(" ","")
    category = category.replace("&","And")
    if category.endswith("s"):
        category = category[:-1]
    st = [s for s in schemaSubTypes if category.lower() in s.lower()]
    t = [s for s in schemaTypes if category.lower() in s.lower()]
    if st != [] :
        g.add((venue, RDF.type, URIRef(schema + st[0])))
        if cat == 1:
            g.remove((venue, RDF.type, schema.localBusiness))
        else:
            cat = 1
    elif t != []:
        g.add((venue, RDF.type, URIRef(schema + t[0])))
        if cat == 1:
            g.remove((venue, RDF.type, schema.localBusiness))
        else:
            cat = 1
    else:
        if cat == 0:
            g.add((venue, RDF.type, schema.localBusiness))
            addProp = BNode()
            g.add((venue,schema.additionalProperty, addProp))
            g.add((addProp, schema.name, Literal('category')))
            g.add((addProp, schema.value, Literal(category)))
            cat = 1
        else:       
            addProp = BNode()
            g.add((venue,schema.additionalProperty, addProp))
            g.add((addProp, schema.name, Literal('category')))
            g.add((addProp, schema.value, Literal(category)))

g.add((venue, schema.name, Literal(response[1]['Name'], lang='en')))

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
g.add((rating, RDF.type, schema.AggregateRating))
g.add((rating, schema.ratingValue,Literal(response[1]['RatingYelp'], datatype=XSD.decimal)))
g.add((rating, schema.reviewCount, Literal(response[1]['ReviewCountYelp'],datatype = XSD.integer)))
g.add((rating, schema.author, Literal('Yelp')))

identifier = BNode()
g.add((venue, schema.identifier, identifier))
g.add((identifier, RDF.type, schema.PropertyValue))
g.add((identifier, schema.propertyID, Literal('BusinessIdYelp')))
g.add((identifier, schema.value,Literal(response[1]['BusinessIdYelp'])))

print g.serialize(format='turtle')

