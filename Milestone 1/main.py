# Import useful libs
from rdflib import Graph, Namespace, URIRef, Literal, XSD, RDF 


# import my own python RDF files
import RDF_conversion_Yelp
import RDF_conversion_Tripadvisor
import RDF_conversion_FSQ


Yelp_graph = RDF_conversion_Yelp.YELP_RDF(5)


TripAdv_graph = RDF_conversion_Tripadvisor.TripAdv_RDF(5)

FSQ_graph = RDF_conversion_FSQ.RDF_FSQ(5)


main_graph = Yelp_graph + TripAdv_graph + FSQ_graph

main_graph.serialize(destination='experiment_1.ttl', format='turtle')
