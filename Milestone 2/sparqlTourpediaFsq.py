# -*- coding: utf-8 -*-
"""
Created on Fri May 04 11:33:03 2018

@author: Maria
"""

from math import sin, cos, sqrt, atan2, radians
from SPARQLWrapper import SPARQLWrapper, JSON

def getDistance(p1, p2):
        # approximate radius of earth in km
        R = 6373.0
        
        lat1 = radians(p1.lat)
        lon1 = radians(p1.long)
        lat2 = radians(p2.lat)
        lon2 = radians(p2.long)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance

"""
first retrieve all the concepts used in the Tourpedia dataset

"""
    
sparql = SPARQLWrapper('https://api.demo.triply.cc/datasets/wouter/tourpedia/services/tourpedia/sparql')
sparql.setQuery("""
                SELECT DISTINCT ?class
                WHERE {
                       [] a ?class }		
                        """)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

concepts1 = [results["results"]["bindings"][i]["class"]["value"] for i in range(0,len(results["results"]["bindings"]))]

"""
now retrieve all concepts used in our dataset

"""

sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
sparql.setQuery("""
    
    select distinct ?class  where {
            []  a ?class
            } 
                """)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

concepts2 = [results["results"]["bindings"][i]["class"]["value"] for i in range(0,len(results["results"]["bindings"]))]

"""
now try to match concepts from the two ontologies one by one

"""    
    
for i in range(0,20):  
    sparql = SPARQLWrapper('https://api.demo.triply.cc/datasets/wouter/tourpedia/services/tourpedia/sparql')
    sparql.setQuery("""PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                SELECT ?lat, ?long, ?s
                WHERE {
                        ?s ns:latitude ?lat . 
                        ?s ns:longitude ?long .
                        ?s a <""" + concepts1[i] + """> }""") 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
#    for j in range(0,len(concepts2)):
                    
                          