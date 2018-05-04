# -*- coding: utf-8 -*-
"""
Created on Thu May 03 16:36:57 2018

@author: Maria
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import math

def JaccSymSPARQL(c1,c2):
    
    sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql/")
    sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/> 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX schema: <http://schema.org/>
    select distinct ?s  where {
            ?s  a """ + c1 + """
            } 
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjects1 = [results["results"]["bindings"][i]["s"]["value"] for i in range(0,len(results["results"]["bindings"]))]

    sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/> 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX schema: <http://schema.org/>
    select distinct ?s  where {
            ?s  a """ + c2 + """
            } 
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjects2 = [results["results"]["bindings"][i]["s"]["value"] for i in range(0,len(results["results"]["bindings"]))]
    
    intersection = len(set(subjects1).intersection(set(subjects2)))

    union = len(list(set(subjects1).union(set(subjects2))))
    
    if union == 0:
        union = 1
        
    print(union)
    print(intersection)
    Jaccard = math.sqrt(intersection * (intersection - 0.8)) / union
    return Jaccard