from research_vocabs.concepts import ConceptScheme


class SimpleLithology(ConceptScheme):
    source = "simple_lithology.ttl"


class BoreholeDrilling(ConceptScheme):
    source = "boreholedrillingmethod.ttl"


class BoreholeDrillingNT(ConceptScheme):
    source = "drillingmethod.nt"


for c in BoreholeDrillingNT.choices:
    print(c)
