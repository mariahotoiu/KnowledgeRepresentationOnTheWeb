# -*- coding: utf-8 -*-
"""
Created on Tue May 01 13:54:41 2018

@author: Maria
"""

import requests

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF, BNode

#first retrieve all classes from our dataset
sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
sparql.setQuery("""
    
    select distinct ?class  where {
            []  a ?class
            } 
                """)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

classesOwn = [results["results"]["bindings"][i]["class"]["value"] for i in range(0,len(results["results"]["bindings"]))]


g = Graph()
owl  = Namespace("http://www.w3.org/2002/07/owl#")
g.bind('owl', owl)

#now for each class, find all equivalent classes from the LOD

for cls in classesOwn:
    cls = "<" + cls + ">"
    print cls
    params = {
              'o':cls,
              'p':'owl:equivalentClass'
            }
    
    response = requests.get('https://hdt.lod.labs.vu.nl/triple', params=params)
    if len(response.text) > 0:
        classesLod = response.text.split(' ')
        classesLod = [classesLod[i] for i in range(0,len(classesLod),4) ]
        for r in classesLod:
            r = r.replace('.\n','')
            if (len(r)>0):
                cls = cls.replace('<','').replace('>','')  
                r = r.replace('<','').replace('>','')  
                print r 
                try:
                    r = URIRef(r)
                    g.add((URIRef(cls), owl.equivalentClass, r))
                except Exception:
                    pass
                

g.serialize(destination='schemaEquivClassesLOD.ttl', format='turtle')        
        


