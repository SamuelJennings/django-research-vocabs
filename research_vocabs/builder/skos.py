from rdflib.namespace import SKOS


class Concept(dict):
    def __init__(self, *args, **kwargs):
        # kwargs must be gettable from SKOS
        new = {}
        for key in kwargs:
            if hasattr(SKOS, key):
                new["skos:" + key] = kwargs.get(key)
            else:
                raise ValueError(f"Invalid SKOS property: {key}")

        super().__init__(*args, **new)


class Collection(Concept):
    def __init__(self, *args, **kwargs):
        self.ordered = kwargs.pop("ordered", False)

        # make sure that either "member" or "members" is in kwargs
        if "member" not in kwargs and "members" not in kwargs:
            raise ValueError("A Collection must specify one or more members.")

        # if "members" is in kwargs, move it to "member"
        if "members" in kwargs:
            kwargs["member"] = kwargs.pop("members")

        # if "member" is not a list, raise an error
        if not isinstance(kwargs["member"], list):
            raise ValueError("A Collection's member/s must be a list.")

        super().__init__(*args, **kwargs)
