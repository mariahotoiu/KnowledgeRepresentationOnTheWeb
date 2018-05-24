# -*- coding: utf-8 -*-
"""
Created on Tue May 01 13:54:41 2018

@author: Maria
"""

import requests

from SPARQLWrapper import SPARQLWrapper, JSON

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

equivs = {}

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
        equivs[cls] = []
        for r in classesLod:
            r = r.replace('.\n','')
            equivs[cls].append(r)
        print equivs[cls]


