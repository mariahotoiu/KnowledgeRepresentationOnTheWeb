# -*- coding: utf-8 -*-
"""
Created on Tue May 01 14:32:03 2018

@author: Maria
"""
import requests

def JaccSim(c1,c2):
    params1 = (
    ('p', 'rdf:type'),
    ('o', c1),
    )

    response1 = requests.get('https://hdt.lod.labs.vu.nl/triple', params=params1)
    response1 = response1.text.split(' ')
    print response1[0]
    
    params2 = (
    ('p', 'rdf:type'),
    ('o', c2),
    )
                                
    response2 = requests.get('https://hdt.lod.labs.vu.nl/triple', params=params2)
    response2 = response2.text.split(' ')
    print response2[0]
    
    for i in range(4,len(response1),4):
        response1[i] = response1[i][2:]
        
    
    
    for i in range(4,len(response2),4):
        response2[i] = response2[i][2:]
        
    
    objects1 = [response1[i] for i in range(0,len(response1),4)]      
    objects2 = [response2[i] for i in range(0,len(response2),4)]  
    
    intersection = len(set(objects1).intersection(set(objects2)))

    union = len(list(set(objects1).union(set(objects2))))
    
    if union == 0:
        union = 1
        
    print(union)
    print(intersection)

    Jaccard = float(intersection) / union
    return Jaccard
    
    
    