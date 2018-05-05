# -*- coding: utf-8 -*-
"""
Created on Sat May 05 15:59:38 2018

@author: Maria
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import similarityFsqTourpedia as simFunc

"""
first retrieve all the concepts used in the Tourpedia dataset for defining venues

"""
    
sparql = SPARQLWrapper('https://api.demo.triply.cc/datasets/wouter/tourpedia/services/tourpedia/sparql')
sparql.setQuery("""
                PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                SELECT DISTINCT ?class
                WHERE {
                       ?s a ?class .
                       ?s ns:latitude [] .
                       ?s ns:longitude []
                       }		
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

simExample = simFunc.similarity(concepts1[0],concepts2[0])
print simExample