# -*- coding: utf-8 -*-
"""
Created on Sat May 05 15:19:51 2018

@author: Maria
"""

from math import sin, cos, sqrt, atan2, radians
from SPARQLWrapper import SPARQLWrapper, JSON


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


def similarity(c1,c2):
    sparql = SPARQLWrapper('https://api.demo.triply.cc/datasets/wouter/tourpedia/services/tourpedia/sparql')
    sparql.setQuery("""PREFIX ns: <http://www.w3.org/2006/vcard/ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>

                SELECT ?lat, ?long, ?s, ?page
                WHERE {
                        ?s ns:latitude ?lat . 
                        ?s ns:longitude ?long .
                        ?s dbo:wikiPageExternalLink ?page .
                        ?s a <""" + c1 + """> }""") 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsTp = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    latitudesTp = [results["results"]["bindings"][ii]["lat"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    longitudesTp = [results["results"]["bindings"][ii]["long"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    pagesTp = [results["results"]["bindings"][ii]["page"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    
    sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
    sparql.setQuery("""   
                        PREFIX schema: <http://schema.org/>
                        SELECT ?s ?lat ?long  ?id
                        WHERE {
                                ?s a <""" + c2 + """> .
                                ?s schema:geo ?coord.
                                ?coord schema:latitude ?lat.
                                ?coord schema:longitude ?long .
                                ?s schema:identifier ?ident .
                                ?ident schema:value ?id
                                }""")
                        
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjectsFsq = [results["results"]["bindings"][ii]["s"]["value"] for ii in range(0,len(results["results"]["bindings"]))] 
    latitudesFsq = [results["results"]["bindings"][ii]["lat"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    longitudesFsq = [results["results"]["bindings"][ii]["long"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    idsFsq = [results["results"]["bindings"][ii]["id"]["value"] for ii in range(0,len(results["results"]["bindings"]))]
    intersect = []
    union = []
    inst1={}
    inst2={}
        
    for sTp, latTp, longTp, pageTp in zip(subjectsTp,latitudesTp, longitudesTp,pagesTp):
            idTp = 0
            if sTp not in union:
                union.append(sTp)
            if 'foursquare' in pageTp:
                pageSplit = pageTp.split('/')
                idTp = pageSplit[len(pageSplit)-1]
            if idTp != 0: 
                if idTp in idsFsq:
                    intersect.append(sTp)
                    index = idsFsq.index(idTp)
                    idsFsq.remove(idsFsq[index])
                    subjectsFsq.remove(subjectsFsq[index])
                    latitudesFsq.remove(latitudesFsq[index])
                    longitudesFsq.remove(longitudesFsq[index])
        
            else:                
                for sFsq, latFsq, longFsq in zip(subjectsFsq, latitudesFsq, longitudesFsq):
                    if sFsq not in union:
                        union.append(sFsq)
                    
                    if round(float(latFsq),3) == round(float(latTp),3) and \
                            round(float(longFsq),3) == round(float(longTp),3):
                                inst1=dict(zip(['latitude','longitude'],[latFsq,longFsq]))
                                inst2=dict(zip(['latitude','longitude'],[latTp,longTp]))
                                d = getDistance(inst1,inst2)
                                if d <= 0.05:
                                    intersect.append(sTp)
                                                    
    union = len(set(union))
    intersect = len(set(intersect))
    return intersect / union   

