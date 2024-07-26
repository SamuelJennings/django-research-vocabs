from rdflib import Graph

g = Graph().parse("https://google.com/incorrect_source.ttl")
print(g)
