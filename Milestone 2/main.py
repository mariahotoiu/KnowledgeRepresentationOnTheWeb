import similarityWithIdOnly_T as simID
import similarityFsqTourpedia_T as simGEO
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import pickle


parser = argparse.ArgumentParser(description='Process info.')
parser.add_argument('--geouser', default=0,
                        help='Number of dimensions. Default is False.')
args = parser.parse_args()
print(args.geouser)





if int(args.geouser) == 1:

    entire_list_matches = []
    print("Geo Only")
    with open("results_geo.csv", "w") as results:
        result = simGEO.similarity_geo_only("http://protege.cim3.net/file/pub/ontologies/travel/travel.owl#Sightseeing","http://schema.org/AmusementPark")
        linestr = "http://protege.cim3.net/file/pub/ontologies/travel/travel.owl#Sightseeing, http://schema.org/AmusementPark"+ ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
        entire_list_matches.append(result[8])
        print(linestr)
        results.write(linestr)
        result = simGEO.similarity_geo_only("http://dbpedia.org/ontology/Restaurant","http://schema.org/FastFoodRestaurant")
        linestr = "http://dbpedia.org/ontology/Restaurant, http://schema.org/FastFoodRestaurant" + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
        entire_list_matches.append(result[8])
        print(linestr)
        results.write(linestr)
        result = simGEO.similarity_geo_only("http://dbpedia.org/ontology/Restaurant","http://schema.org/LocalBusiness")
        linestr = "http://dbpedia.org/ontology/Restaurant, http://schema.org/LocalBusiness" + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
        entire_list_matches.append(result[8])
        print(linestr)
        results.write(linestr)
        result = simGEO.similarity_geo_only("http://wafi.iit.cnr.it/angelica/Hontology.owl#Accommodation","http://schema.org/Hotel")
        linestr = "http://wafi.iit.cnr.it/angelica/Hontology.owl#Accommodation, http://schema.org/Hotel"+ ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
        entire_list_matches.append(result[8])
        print(linestr)
        results.write(linestr)

    output = open('data_geo.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(entire_list_matches, output)



else:
    print("ID and geo")
    simIDonly = False

    entire_list_matches = []
    results_list = []

    schema_types_fsq_food = ["http://schema.org/Restaurant", "http://schema.org/FastFoodRestaurant"]
    schema_types_tourpedia_food = ["http://dbpedia.org/ontology/Restaurant"]

    schema_types_fsq_acc = ["http://schema.org/Hostel", "http://schema.org/Motel", "http://schema.org/Hotel" ]
    schema_types_tourpedia_acc = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#Accommodation"]

    schema_types_fsq_sight = ["http://schema.org/NightClub" , "http://schema.org/Casino", "http://schema.org/AmusementPark"]
    schema_types_tourpedia_sight = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#PointsOfInterest","http://protege.cim3.net/file/pub/ontologies/travel/travel.owl#Sightseeing"]

    schema_types_fsq_loc = ["http://schema.org/LocalBusiness"]
    schema_types_tourpedia_loc = ["http://wafi.iit.cnr.it/angelica/Hontology.owl#PointsOfInterest","http://dbpedia.org/ontology/Restaurant","http://protege.cim3.net/file/pub/ontologies/travel/travel.owl#Sightseeing", "http://purl.org/goodrelations/v1#ProductOrService"]



    with open("results.csv", "w") as results:
        if simIDonly == True:
            results.write("tourpedia, foursquare, setsize(tourpedia), setsize(FourSquare), len(union), len(intersect), Jaccard, correctedJacc, Dice, overlap Coef \n")
        else:
            results.write("tourpedia, foursquare, setsize(tourpedia), setsize(FourSquare), len(union), len(intersect), Jaccard, correctedJacc, Dice, overlap Coef, setsize(tourpedia), setsize(FourSquare), len(union) geo, len(intersect)  geo, Jaccard  geo, correctedJacc  geo , Dice geo, overlap Coef geo\n")
        for c1 in schema_types_tourpedia_acc:
            for c2 in schema_types_fsq_acc:
                print(c1, c2)
                if simIDonly == True:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                else:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7])
                    entire_list_matches.append(result[8])

                    result = simGEO.similarity(c1, c2)
                    linestr += str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                results.write(linestr)

        for c1 in schema_types_tourpedia_food:
            for c2 in schema_types_fsq_food:
                print(c1, c2)
                if simIDonly == True:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                else:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7])
                    entire_list_matches.append(result[8])
                    
                    result = simGEO.similarity(c1, c2)
                    linestr += str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                results.write(linestr)

        for c1 in schema_types_tourpedia_sight:
            for c2 in schema_types_fsq_sight:
                print(c1, c2)
                if simIDonly == True:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                else:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7])
                    entire_list_matches.append(result[8])
                    result = simGEO.similarity(c1, c2)
                    linestr += str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                results.write(linestr)
        for c1 in schema_types_tourpedia_loc:
            for c2 in schema_types_fsq_loc:
                print(c1, c2)
                if simIDonly == True:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                else:
                    result = simID.similarity(c1, c2)
                    linestr = c1 + ", "+ c2 + ", " + str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7])
                    entire_list_matches.append(result[8])
                    
                    result = simGEO.similarity(c1, c2)
                    linestr += str(result[0]) + ", "+ str(result[1])+ ", "+ str(result[2])+ ", "+ str(result[3]) + ", "+ str(result[4]) + ", "+ str(result[5]) + ", "+ str(result[6]) + ", "+ str(result[7]) + "\n"
                results.write(linestr)

    output = open('data_id.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(entire_list_matches, output)
