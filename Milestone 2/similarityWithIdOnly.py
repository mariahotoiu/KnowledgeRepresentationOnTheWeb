# -*- coding: utf-8 -*-
"""
Created on Sat May 05 17:57:01 2018

@author: Maria
"""

from math import sqrt
from SPARQLWrapper import SPARQLWrapper, JSON

def similarity(c1,c2):
    sparql = SPARQLWrapper('http://localhost:5820/tourPedia/query')
    sparql.setQuery("""PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>

                SELECT ?s ?page
                WHERE { ?s a <""" + c1 + """> .
                        ?s dbo:wikiPageExternalLink ?page .
                        FILTER CONTAINS(STR(?page),'foursquare')
                         }""") 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsTp = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    pagesTp = [results["results"]["bindings"][ii]["page"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    print(len(subjectsTp))
    sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
    sparql.setQuery("""   
                        PREFIX schema: <http://schema.org/>
                        SELECT ?s ?id WHERE {
                                ?s a <""" + c2 + """> .
                                ?s schema:identifier ?ident .
                                ?ident schema:value ?id
                                }""")
                        
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsFsq = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    idsFsq = [results["results"]["bindings"][ii]["id"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    intersect = []
    union = []
        
    for sTp, pageTp in zip(subjectsTp, pagesTp):
            idTp = 0
            if sTp not in union:
                union.append(sTp)
           
            pageSplit = pageTp.split('/')
            idTp = pageSplit[len(pageSplit)-1]
            if idTp in idsFsq:
                    intersect.append(sTp)
                    index = idsFsq.index(idTp)
                    idsFsq.remove(idsFsq[index])
                    subjectsFsq.remove(subjectsFsq[index])                    
        
                            
    union1 = len(set(union)) + len(set(subjectsFsq))
    intersect1 = len(set(intersect))
    print (union1,intersect1)
    return sqrt(intersect1 * (intersect1 - 0.8)) / union1  

print similarity('http://dbpedia.org/ontology/Restaurant', 'http://schema.org/localBusiness')
