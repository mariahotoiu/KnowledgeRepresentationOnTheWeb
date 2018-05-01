# -*- coding: utf-8 -*-


import requests


params = (
	("p" ,"rdf:type"), 
	("o", "dbo:book")
)


response_1 = requests.get("https://hdt.lod.labs.vu.nl/triple?p=rdf:type&o=dbo:Book",params=params)

response_2 = requests.get("https://hdt.lod.labs.vu.nl/triple?p=rdf:type&o=schema:Book",params=params)

complete_response_1 = []
for elem in response_1:
	elems = elem.split("> <")
	for elem in elems:
		if "http://ar.dbpedia.org/resource/" in elem: 
			complete_response_1.append(elem.split("http://ar.dbpedia.org/resource/")[-1])


complete_response_2 = []
for elem in response_2:
	elems = elem.split("> <")
	for elem in elems:
		if "http://ar.dbpedia.org/resource/" in elem: 
			complete_response_2.append(elem.split("http://ar.dbpedia.org/resource/")[-1])


intersection = 0

for elem_1 in set(complete_response_2):
	if elem_1 in set(complete_response_1):
		intersection += 1


union = len(set(complete_response_1))+ len(set(complete_response_2)) - intersection
print(union)

Jaccard = float(intersection) / union

print(Jaccard)
