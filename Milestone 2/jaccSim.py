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
    
    r = requests.get('https://hdt.lod.labs.vu.nl/triple', params=params1)
    response1 = r.text
#    while 'next' in r.links.keys():  
    if 'next' in r.links.keys():    
        r = requests.get(r.links['next']['url'], params = params1)  
        response1 += r.text
    response1 = response1.split(' ')
    response1 = response1[:-1]
#    print len(response1)
    
    params2 = (
    ('p', 'rdf:type'),
    ('o', c2),
    )
                             
    r = requests.get('https://hdt.lod.labs.vu.nl/triple', params=params2)
    response2 = r.text
#    while 'next' in r.links.keys():
    if 'next' in r.links.keys():
        r = requests.get(r.links['next']['url'], params = params1)  
        response2 += r.text
    
    response2 = response2.split(' ')
    response2 = response2[:-1]
#    print response2[0]
    
    for i in range(4,len(response1),4):
        response1[i] = response1[i][2:]
        
    
    
    for i in range(4,len(response2),4):
        response2[i] = response2[i][2:]
        
    
    subjects1 = [response1[i] for i in range(0,len(response1),4)]      
    subjects2 = [response2[i] for i in range(0,len(response2),4)]  
    
    intersection = len(set(subjects1).intersection(set(subjects2)))

    union = len(list(set(subjects1).union(set(subjects2))))
    
    if union == 0:
        union = 1
        
    print(union)
    print(intersection)
    Jaccard = float(intersection) / union
    return Jaccard
    
#    length1 = requests.get('https://hdt.lod.labs.vu.nl/triple/count', params=params1)
#    params1 = params1 + ('page_length',length1)    
#length2 = requests.get('https://hdt.lod.labs.vu.nl/triple/count', params=params2)       
