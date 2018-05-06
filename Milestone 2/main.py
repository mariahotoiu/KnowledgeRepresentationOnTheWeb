import similarityWithIdOnly as simID
import similarityFsqTourpedia as simGEO
import os
from SPARQLWrapper import SPARQLWrapper, JSON

results_list = []

schema_types_fsq_food = ["http://schema.org/Restaurant", "http://schema.org/FastFoodRestaurant"]
schema_types_tourpedia_food = ["http://dbpedia.org/ontology/Restaurant"]

schema_types_fsq_acc = ["http://schema.org/Hostel", "http://schema.org/Motel", "http://schema.org/Hotel" ]
schema_types_tourpedia_acc = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#Accommodation","http://purl.org/acco/ns#Accommodation"]

schema_types_fsq_sight = ["http://schema.org/NightClub" , "http://schema.org/Casino", "http://schema.org/AmusementPark"]
schema_types_tourpedia_sight = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#PointsOfInterest","http://protege.cim3.net/file/pub/ontologies/travel/travel.owl#Sightseeing"]

schema_types_fsq_loc = ["http://schema.org/LocalBusiness"]
schema_types_tourpedia_loc = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#PointsOfInteres","http://dbpedia.org/ontology/Restaurant","http://purl.org/acco/ns#Accommodation" ]


with open("results.txt", "w") as results:
    results.write("tourpedia, foursquare, len(union), len(intersect), Jaccard, correctedJacc \n")
    for c1 in schema_types_tourpedia_food:
        for c2 in schema_types_fsq_food:
            print(c1, c2)
            result = simID.similarity(c1, c2)
            linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + "\n"
            results.write(linestr)
    for c1 in schema_types_tourpedia_acc:
        for c2 in schema_types_fsq_acc:
            result = simID.similarity(c1, c2)
            linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + "\n"
            results.write(linestr)
    for c1 in schema_types_tourpedia_sight:
        for c2 in schema_types_fsq_sight:
            result = simID.similarity(c1, c2)
            linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + "\n"
            results.write(linestr)
    for c1 in schema_types_tourpedia_loc:
        for c2 in schema_types_fsq_loc:
            result = simID.similarity(c1, c2)
            linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + "\n"
            results.write(linestr)