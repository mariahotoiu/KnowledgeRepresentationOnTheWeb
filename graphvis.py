from rdflib import RDF, RDFS, Graph
import rdflib.util as util
from rdflib.tools import rdfs2dot, rdf2dot
import io
import sys
import os


# Schema: 597 Types, 875 Properties, and 114 Enumeration values


g = Graph()

g.parse("CompleteVenuesTTL.ttl", format="turtle")

print("is connected:  " + str(g.connected()))


classes = []
for elem in g.predicates():
	if "http://foursq" in elem:
		classes.append(elem)


print(len(set(classes)))
print(set(classes))
classes = []
for elem in g.objects():
	if "http://foursq" in elem:
		classes.append(elem)


print(len(set(classes)))
print(set(classes))


classes = []
for elem in g.subjects():
	if "http://foursq" in elem:
		classes.append(elem)


print(len(set(classes)))
print(set(classes))
