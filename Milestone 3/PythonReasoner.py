import requests
import os
import logging


from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF, BNode




#first retrieve all classes from our dataset
sparql_reasoner = SPARQLWrapper("http://localhost:5820/myDB/query")
sparql_no_reasoner = SPARQLWrapper("http://localhost:5820/myDB/query")
# Check if database can be called.
if os.environ['USERNAME'] == "thoma":
    sparql_reasoner = SPARQLWrapper("http://localhost:5820/FSQVenues/query")
    sparql_no_reasoner = SPARQLWrapper("http://localhost:5820/FSQVenues/query")

query = """
select (count(distinct ?o) as ?count) where {[] a ?o}
                """



sparql_reasoner.setQuery(query)
sparql_reasoner.setReturnFormat(JSON)

sparql_reasoner.addParameter('reasoning','true')

results = sparql_reasoner.query().convert()


if "count" in query:
	print(results["results"]["bindings"][0]["count"]["value"])
elif "ask" in query: 
	print(results["boolean"])
else:
	try:
		for elem in results["results"]["bindings"]:
			print(elem)
	except:
		print("can not distinguish what query was written")


sparql_no_reasoner.setQuery(query)
sparql_no_reasoner.setReturnFormat(JSON)

sparql_no_reasoner.addParameter('reasoning','false')

results = sparql_no_reasoner.query().convert()

if "count" in query:
	print(results["results"]["bindings"][0]["count"]["value"])
elif "ask" in query: 
	print(results["boolean"])
else:
	try:
		for elem in results["results"]["bindings"]:
			print(elem)
	except:
		print("can not distinguish what query was written")






#first retrieve all classes from our dataset
sparql_reasoner = SPARQLWrapper("http://localhost:5820/myDB/query")
sparql_no_reasoner = SPARQLWrapper("http://localhost:5820/myDB/query")
# Check if database can be called.
if os.environ['USERNAME'] == "thoma":
    sparql_reasoner = SPARQLWrapper("http://localhost:5820/tourPedia/query")
    sparql_no_reasoner = SPARQLWrapper("http://localhost:5820/tourPedia/query")

query = """
select (count(distinct ?o) as ?count) where {[] a ?o}
                """



sparql_reasoner.setQuery(query)
sparql_reasoner.setReturnFormat(JSON)

sparql_reasoner.addParameter('reasoning','true')

results = sparql_reasoner.query().convert()


if "count" in query:
	print(results["results"]["bindings"][0]["count"]["value"])
elif "ask" in query: 
	print(results["boolean"])
else:
	try:
		for elem in results["results"]["bindings"]:
			print(elem)
	except:
		print("can not distinguish what query was written")


sparql_no_reasoner.setQuery(query)
sparql_no_reasoner.setReturnFormat(JSON)

sparql_no_reasoner.addParameter('reasoning','false')

results = sparql_no_reasoner.query().convert()

if "count" in query:
	print(results["results"]["bindings"][0]["count"]["value"])
elif "ask" in query: 
	print(results["boolean"])
else:
	try:
		for elem in results["results"]["bindings"]:
			print(elem)
	except:
		print("can not distinguish what query was written")