# -*- coding: utf-8 -*-
"""
Created on Fri May 04 11:33:03 2018

@author: Maria
"""

from math import sin, cos, sqrt, atan2, radians
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from collections import defaultdict

def getDistance(p1, p2):
        # approximate radius of earth in km
        R = 6373.0
        
        lat1 = radians(float(p1['latitude']))
        lon1 = radians(float(p1['longitude']))
        lat2 = radians(float(p2['latitude']))
        lon2 = radians(float(p2['longitude']))
        
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
get all instances and their lat/long for Tourpedia

"""    
dfTp = pd.DataFrame(columns = ['subject', 'latitude', 'longitude', 'class'])
    
for i in range(0,len(concepts1)): 
    concept = concepts1[i]
    sparql = SPARQLWrapper('https://api.demo.triply.cc/datasets/wouter/tourpedia/services/tourpedia/sparql')
    sparql.setQuery("""PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                SELECT ?lat, ?long, ?s
                WHERE {
                        ?s ns:latitude ?lat . 
                        ?s ns:longitude ?long .
                        ?s a <""" + concepts1[i] + """> }""") 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsTp = [results["results"]["bindings"][i]["s"]["value"] for i in range(0,len(results["results"]["bindings"]))] 
    latitudesTp = [results["results"]["bindings"][i]["lat"]["value"] for i in range(0,len(results["results"]["bindings"]))]
    longitudesTp = [results["results"]["bindings"][i]["long"]["value"] for i in range(0,len(results["results"]["bindings"]))]
    conceptsTp = [concept for number in xrange(len(subjectsTp))]
    entry = pd.DataFrame(list(zip(subjectsTp,latitudesTp,longitudesTp,conceptsTp)), \
                         columns = ['subject', 'latitude', 'longitude', 'class'])
    dfTp = pd.concat([dfTp,entry])

dfTp = dfTp.dropna(axis = 0, how = 'any')

"""
now get all instances and their lat/long for Foursquare

"""


dfFsq = pd.DataFrame(columns = ['subject', 'latitude', 'longitude', 'class'])    
for j in range(0,len(concepts2)):
        concept = concepts2[j]
        sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
        sparql.setQuery("""   
                        PREFIX schema: <http://schema.org/>
                        SELECT ?s ?lat ?long
                        WHERE {
                                ?s a <""" + concepts2[j] + """> .
                                ?s schema:geo ?coord.
                                ?coord schema:latitude ?lat.
                                ?coord schema:longitude ?long
                                }""")
                        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        subjectsFsq = [results["results"]["bindings"][i]["s"]["value"] for i in range(0,len(results["results"]["bindings"]))] 
        latitudesFsq = [results["results"]["bindings"][i]["lat"]["value"] for i in range(0,len(results["results"]["bindings"]))]
        longitudesFsq = [results["results"]["bindings"][i]["long"]["value"] for i in range(0,len(results["results"]["bindings"]))]
        conceptsFsq = [concept for number in xrange(len(subjectsTp))]
        entry = pd.DataFrame(list(zip(subjectsFsq,latitudesFsq,longitudesFsq,conceptsFsq)), \
                         columns = ['subject', 'latitude', 'longitude', 'class'])
        dfFsq = pd.concat([dfFsq,entry])

"""
compare concepts 1 by 1 - this script takes a VERY long while to compute, did not check the results yet

     
sim_matrix = defaultdict(dict)  
for i in xrange(len(concepts1)):
    dfTpTemp = dfTp.loc[dfTp['class'] == concepts1[i]]
    for j in xrange(len(concepts2)):
        dfFsqTemp = dfFsq.loc[dfFsq['class'] == concepts2[i]]
        intersect = 0
        union = 0
        for index,inst1 in dfFsqTemp.iterrows():
            for index,inst2 in dfTpTemp.iterrows():
                
                d = getDistance(inst1,inst2)
                if d <= 0.01:
                    intersect += 1
                    union += 1
                else:
                    union += 2
        union = max(1,union)
        sim_matrix[concepts1[i]][concepts2[j]] = intersect / union     
"""                    
                          
