from django.utils.translation import gettext_lazy as _
from rdflib.namespace import RDF, SKOS

from research_vocabs.concepts import (
    ConceptSchemeBuilder,
    LocalConceptScheme,
)


class SimpleLithology(LocalConceptScheme):

    class Meta:
        source = "simple_lithology.ttl"


class ISC2020(LocalConceptScheme):
    class Meta:
        source = "isc2020.ttl"


# class ISC2020(RemoteConceptScheme):
#     class Meta:
#           source = "https://vocabs.ardc.edu.au/registry/api/resource/downloads/1211/isc2020.ttl"


# register vocabulary will include this class in the list of vocabularies that are exposed via the
# vocabularies/ endpoint. This is useful for when you want to expose your custom vocabulary to the
# outside world.


# @register_vocabulary
class MyMaterialsScheme(ConceptSchemeBuilder):
    """An example building my own concept scheme. This is a custom class that extends the CustomConceptScheme class. It is used to define a custom concept scheme with custom concepts and collections."""

    Wood = {
        SKOS.prefLabel: _("Wood"),
        SKOS.altLabel: [_("Timber"), _("Lumber")],
        SKOS.definition: _(
            "A hard fibrous material that forms the main substance of the trunk or branches of a tree or shrub."
        ),
    }

    Metal = {
        RDF.type: SKOS.Concept,
        SKOS.prefLabel: _("Metal"),
        SKOS.altLabel: [_("Metallic")],
        SKOS.definition: _(
            "A solid material that is typically hard, shiny, malleable, fusible, and ductile, with good electrical and thermal conductivity."
        ),
        # SKOS.broader: Wood,
    }

    class Meta:
        namespace = "https://heatflow.world/vocabularies/"
        namespace_prefix = "ghfdb"
        conceptscheme = {
            SKOS.altLabel: _("My Material Scheme"),
            SKOS.prefLabel: _("My Materials"),
            SKOS.hasTopConcept: [
                "Wood",
                "Metal",
            ],
        }
        ordered_collections = {"orderedCollectionA": ["Metal", "Plastic", "Wood"]}
        collections = {
            "collectionA": ["Wood", "Metal"],
            "collectionB": ["Wood"],
        }


subcollection = MyMaterialsScheme.as_collection("collectionA")

# print(list(subcollection.choices))

# print(list(SimpleLithology.choices))
# print(list(MyMaterialsScheme.choices))
