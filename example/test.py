import json

from example.vocabularies import ISC2020
from rdflib import RDF, SKOS, Namespace

ISC = Namespace("http://resource.geosciml.org/classifier/ics/ischart/")

g = ISC2020.graph


def collection_members(collection_uri):
    query = f"""
    SELECT ?member
    WHERE {{
      <{collection_uri}> a SKOS:Collection ;
                  SKOS:member ?member .
    }}
    """

    # Execute the query
    return g.query(query, initNs={"SKOS": SKOS, "ISC": ISC})


# members = collection_members(ISC[""])
# for row in members:
#     print(row.concept)


def collection_members(collection_uri):
    return g.triples((collection_uri, SKOS.member, None))


def collection_concepts(collection_uri):
    """Returns a list of unstructured SKOS:Concepts in a collection."""
    concepts = []
    for subj, pred, obj in collection_members(collection_uri):
        if SKOS.Concept in g.objects(obj, RDF.type):
            concepts.append(obj)
        else:
            concepts += collection_concepts(obj)

    return concepts


def get_members(collection_uri):
    members = {}
    for subj, pred, obj in collection_members(collection_uri):
        if SKOS.Collection in g.objects(obj, RDF.type) or SKOS.OrderedCollection in g.objects(obj, RDF.type):
            # recursively get members of collections
            value = get_members(obj)
        else:
            value = g.namespace_manager.normalizeUri(obj)

        label = g.namespace_manager.normalizeUri(subj)

        if label not in members:
            members[label] = []

        members[label].append(value)

    return members


members = get_members(ISC[""])


# members = get_members(ISC[""])


flat_info = []
for c in collection_concepts(ISC.Eons):
    flat_info.append(ISC2020.get_concept_meta(c))

with open("flat_concepts.json", "w") as f:
    json.dump(flat_info, f, indent=2)
