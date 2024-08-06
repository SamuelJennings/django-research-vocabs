from rdflib.namespace import SKOS

# Wood = {
#     "skos:prefLabel": _("Wood"),
#     "skos:altLabel": [_("Timber"), _("Lumber")],
#     "skos:definition": _(
#         "A hard fibrous material that forms the main substance of the trunk or branches of a tree or shrub."
#     ),
# }

class Concept(dict):

    def __init__(self, *args, **kwargs):
        # kwargs must be gettable from SKOS
        for key in kwargs:
            if hasattr(SKOS, key):
                kwargs["skos:" + key] = kwargs.pop(key)

        super().__init__(*args, **kwargs)


c = Concept(prefLabel="Wood", altLabel=["Timber", "Lumber"], definition="A hard fibrous material that forms the main substance of the trunk or branches of a tree or shrub.")

print(c)
