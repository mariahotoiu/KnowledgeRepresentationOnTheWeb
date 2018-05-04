# -*- coding: utf-8 -*-
"""
Created on Thu May 03 12:14:13 2018

@author: Maria
"""


import pandas as pd
import os
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF, BNode


root = 'D:\Cursuri Master\Knowledge Representation on the Web\FSQ'



venues = pd.read_csv(os.path.join(root,'venues.txt'), sep="\t", header=None)
venues.columns = ['BusinessIdFSQ', 'Latitude', 'Longitude', 'CategoryFSQ', 'Country']
   
venuesIT = venues[venues['Country'] == 'IT']
venuesNL = venues[venues['Country'] == 'NL']
venuesDE = venues[venues['Country'] == 'DE']
venuesGB = venues[venues['Country'] == 'GB']
venuesFR = venues[venues['Country'] == 'FR']
venuesAE = venues[venues['Country'] == 'AE']
venuesES = venues[venues['Country'] == 'ES']

venuesArr = [venuesIT, venuesDE, venuesGB, venuesFR, venuesAE, venuesES, venuesNL]
venues = pd.concat(venuesArr)


root2 = 'D:\Cursuri Master\Knowledge Representation on the Web'
with open(os.path.join(root2,'schemaTypes.txt'), "r") as word_list:
    schemaTypes = word_list.read().split('\n')

with open(os.path.join(root2,'schemaSubtypes.txt'), "r") as word_list:
    schemaSubTypes = word_list.read().split('\n')


g = Graph()


yelp =  Namespace("http://yelp.com/")
schema = Namespace("http://schema.org/")
fsq = Namespace('https://foursquare.com/')
g.bind('schema',schema)
g.bind('foursquare',fsq)  

for i in range(0,len(venues)):
        """
        Now for foursquare
        
        """
        url2 = "https://foursquare.com/v/" + venues['BusinessIdFSQ'].iloc[i]
        venue = URIRef(url2)

        category = venues['CategoryFSQ'].iloc[i]
        cat = 0
        
        category = category.replace(" ","")
        category = category.replace("&","And")
        if category.endswith("s"):
                category = category[:-1]
        st = [s for s in schemaSubTypes if category.lower() in s.lower()]
        t = [s for s in schemaTypes if category.lower() in s.lower()]
        if st != [] :
                g.add((venue, RDF.type, URIRef(schema + st[0])))
                if cat == 1:
                    g.remove((venue, RDF.type, schema.LocalBusiness))
                else:
                    cat = 1
        elif t != []:
                g.add((venue, RDF.type, URIRef(schema + t[0])))
                if cat == 1:
                    g.remove((venue, RDF.type, schema.LocalBusiness))
                else:
                    cat = 1
        else:
                if cat == 0:
                    g.add((venue, RDF.type, schema.LocalBusiness))
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
        
        geo = BNode()
        g.add((venue,schema.geo,geo))
        g.add((geo, RDF.type, schema.GeoCoordinates))
        g.add((geo,schema.latitude,Literal(venues['Latitude'].iloc[i], datatype=XSD.decimal)))
        g.add((geo,schema.longitude,Literal(venues['Longitude'].iloc[i], datatype=XSD.decimal)))
        

        identifier = BNode()
        g.add((venue, schema.identifier, identifier))
        g.add((identifier, RDF.type, schema.PropertyValue))
        g.add((identifier, schema.propertyID, Literal('BusinessIdFSQ')))
        g.add((identifier, schema.value,Literal(venues['BusinessIdFSQ'].iloc[i])))
    
g.serialize(destination='FsqMilestone2TTL.ttl', format='turtle')

