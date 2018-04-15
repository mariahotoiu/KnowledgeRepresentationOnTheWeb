from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF
import requests
import json

# create an RDF graph
foursquare_graph = Graph()

foursquare_api_link = "https://api.foursquare.com/v2/venues/"
params = dict(
  client_id="QS20SFPKYDQ5B25XPHE3PI3TKDEQ5KBBBYJBJVOX2B1SGKIR",
  client_secret="3W1AD4PK5W4CON5VVDZTKSPRYJKLWDNZQ01O2CEX0KTDQK5Z",
  v="20180323",
  limit=1)

venueIDs = ["49bbd6c0f964a520f4531fe3", "4ce1863bc4f6a35d8bd2db6c"]
foursquare = Namespace("http://foursquare.com/")

foursquare_graph.bind("foursquare",foursquare)

for venueID in venueIDs:
	response = requests.get(foursquare_api_link+venueID,params=params).json()
	print(response)

	venue_URI = IMDB[venueID]

	print "Created {}".format(venue_URI)
	g.add((venue_URI, RDF.type, IMDB["response"][]))


