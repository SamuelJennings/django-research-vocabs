from django.utils.translation import gettext_lazy as _

from research_vocabs import LocalVocabulary, RemoteVocabulary, VocabularyBuilder
from research_vocabs.registry import vocab_registry


class SimpleLithology(LocalVocabulary):
    class Meta:
        source = "./vocab_data/simple_lithology.ttl"
        default_namespace = "lith"


class ISC2020(RemoteVocabulary):
    class Meta:
        source = "https://vocabs.ardc.edu.au/registry/api/resource/downloads/1211/isc2020.ttl"
        # source = "./vocab_data/isc2020.ttl"


class CustomMaterials(VocabularyBuilder):
    """An example building my own concept scheme. This is a custom class that extends the CustomConceptScheme class. It is used to define a custom concept scheme with custom concepts and collections."""

    Wood = {
        "skos:prefLabel": _("Wood"),
        "skos:altLabel": [_("Timber"), _("Lumber")],
        "skos:definition": _(
            "A hard fibrous material that forms the main substance of the trunk or branches of a tree or shrub."
        ),
    }

    Metal = {
        "skos:prefLabel": _("Metal"),
        "skos:altLabel": [_("Metallic")],
        "skos:definition": _(
            "A solid material that is typically hard, shiny, malleable, fusible, and ductile, with good electrical and thermal conductivity."
        ),
    }

    class Meta:
        name = "materials"
        scheme_attrs = {
            "skos:altLabel": _("Custom Material LocalVocabulary"),
            "skos:prefLabel": _("Custom Materials"),
            "skos:definition": _("A custom concept scheme for materials."),
            "skos:hasTopConcept": [
                "Wood",
                "Metal",
            ],
        }
        namespaces = {
            "mats": "www.example.org/",
        }
        default_namespace = "mats"
        collections = {
            "collectionA": [
                "Wood",
                "Metal",
            ],
            "collectionB": [
                "Wood",
            ],
        }
        ordered_collections = ["collectionA"]


m = CustomMaterials()
vocab_registry.register(m)

# c = m.concepts()[0]

sl = SimpleLithology()

# for concept in sl.concepts():
#     broader = concept.attrs.get(SKOS.broader, [])
#     narrower = concept.attrs.get(SKOS.narrower, [])

#     # print(broader)

#     if isinstance(broader, list) and len(broader) > 1:
#         print(concept)
#         print(broader)
#         print("\n")

# if isinstance(narrower, list) and len(narrower) > 1:
#     print(concept)
#     print(narrower)

# for node in sl.tree():
#     print(node)

# for choice in sl.choices:
# print(choice)
# m = CustomMaterials()

# print(list(m.choices))

# c = Concept("Wood", m)

# print(c["skos.prefLabel"])

# print(c)
# subcollection = CustomMaterials.as_collection("collectionB")
# subcollection = CustomMaterials(collection="collectionB")

# print(list(subcollection.choices))

# print(list(SimpleLithology.choices))
# print(list(CustomMaterials.choices))
