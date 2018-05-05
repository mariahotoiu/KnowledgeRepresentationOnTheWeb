# -*- coding: utf-8 -*-
"""
Created on Sat May 05 17:57:01 2018

@author: Maria
"""

from math import sqrt
from SPARQLWrapper import SPARQLWrapper, JSON
import os

def similarity(c1,c2):
    # Locate the tourpedia database. 
    sparql = SPARQLWrapper('http://localhost:5820/tourPedia/query')

    # Check if the database can be contacted else use different location of the database.
    if os.environ['USERNAME'] == "thoma":
        sparql = SPARQLWrapper('http://localhost:5820/tourPedia/query')

    # Call the query and use the sparql wrapper to call the tourpedia database
    sparql.setQuery("""PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>

                SELECT ?s ?page
                WHERE { ?s a <""" + c1 + """> .
                        ?s dbo:wikiPageExternalLink ?page .
                        FILTER CONTAINS(STR(?page),'foursquare')
                         }""") 

    # Locate the subjects and rewrite them to JSON.
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsTp = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    pagesTp = [results["results"]["bindings"][ii]["page"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    # Print the total amount of subjects
    print(len(subjectsTp))

    # locate the Foursquare database.
    sparql = SPARQLWrapper("http://localhost:5820/myDB/query")

    # Check if database can be called.
    if os.environ['USERNAME'] == "thoma":
        sparql = SPARQLWrapper("http://localhost:5820/FSQVenues/query")

    # Call the query to find all the schema identifiers.
    sparql.setQuery("""   
                        PREFIX schema: <http://schema.org/>
                        SELECT ?s ?id WHERE {
                                ?s a <""" + c2 + """> .
                                ?s schema:identifier ?ident .
                                ?ident schema:value ?id
                                }""")
    # Locate the subjects and rewrite them to json
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsFsq = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    idsFsq = [results["results"]["bindings"][ii]["id"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    
    # Set the intersection and the union
    intersect = []
    union = []
    
    # Loop through all values
    for sTp, pageTp in zip(subjectsTp, pagesTp):
            idTp = 0
            # Append the elements not yet in union
            if sTp not in union:
                union.append(sTp)
            
            pageSplit = pageTp.split('/')
            idTp = pageSplit[len(pageSplit)-1]
            
            # Check if in intersect than add to it.
            if idTp in idsFsq:
                    intersect.append(sTp)
                    index = idsFsq.index(idTp)
                    idsFsq.remove(idsFsq[index])
                    subjectsFsq.remove(subjectsFsq[index])                    
        
    # Calculate the union and intersect.
    union1 = len(set(union)) + len(set(subjectsFsq))
    intersect1 = len(set(intersect))
    print (union1,intersect1)
    return sqrt(intersect1 * (intersect1 - 0.8)) / union1  

# Print the similarity
print similarity('http://dbpedia.org/ontology/Restaurant', 'http://schema.org/LocalBusiness')
