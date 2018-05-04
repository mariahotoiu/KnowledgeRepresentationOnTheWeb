from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:5820/myDB/query")
sparql.setQuery("""
    
    select distinct ?s  where {
            ?s  a []
            } LIMIT 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])