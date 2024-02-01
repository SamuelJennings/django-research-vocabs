# SKOS Primer

The Simple Knowledge Organization System (SKOS) is a W3C recommendation for representing knowledge organization systems (KOS) using the Resource Description Framework (RDF). It provides a way to represent concepts and their relationships in a machine-readable format. SKOS is designed to be used in conjunction with other RDF vocabularies, such as Dublin Core and FOAF.

## SKOS Concept Schemes

In the context of SKOS (Simple Knowledge Organization System), a "concept scheme" refers to a collection of concepts that are organized and grouped together based on a common theme or purpose. It provides a way to structure and organize related concepts within a specific domain or knowledge context. A concept scheme is essentially a set of concepts that are semantically related and are meant to be used together.

Key points about concept schemes in SKOS:

1. **Definition:** A concept scheme is formally defined in SKOS as a set of concepts, possibly including statements about semantic relationships between those concepts.

2. **Hierarchy:** Concept schemes often have a hierarchical structure, where concepts are organized into broader and narrower relationships. This hierarchy helps represent the broader context of concepts within the scheme.

3. **Labeling and Documentation:** Concept schemes can have labels, notations, and other documentation elements to provide additional information about the scheme and its intended use.

4. **Use Cases:** Concept schemes are useful for representing various types of knowledge organization systems, such as taxonomies, thesauri, and classification schemes. They help to capture the organizational structure of concepts within a specific knowledge domain.

5. **Example:** In a concept scheme related to the field of biology, the scheme might include concepts for different species, with hierarchical relationships indicating taxonomic classifications.

In SKOS, the main elements related to concept schemes are:

- **skos:ConceptScheme:** The SKOS vocabulary includes the concept scheme class, represented by the URI (Uniform Resource Identifier) `http://www.w3.org/2004/02/skos/core#ConceptScheme`. Instances of this class represent concept schemes.

- **skos:inScheme:** This property is used to link a concept to the concept scheme to which it belongs. It indicates that the concept is a member of the specified concept scheme.

Here's a simple example in Turtle syntax:

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://example.org/myConceptScheme>
  a skos:ConceptScheme ;
  skos:prefLabel "My Concept Scheme"@en .

<http://example.org/Concept1>
  a skos:Concept ;
  skos:prefLabel "Concept 1"@en ;
  skos:inScheme <http://example.org/myConceptScheme> .

<http://example.org/Concept2>
  a skos:Concept ;
  skos:prefLabel "Concept 2"@en ;
  skos:inScheme <http://example.org/myConceptScheme> .
```

In this example, `<http://example.org/myConceptScheme>` represents a concept scheme, and `<http://example.org/Concept1>` and `<http://example.org/Concept2>` are concepts within that scheme. The `skos:inScheme` property is used to associate each concept with the concept scheme.


## SKOS Concepts

In the context of SKOS (Simple Knowledge Organization System), a "concept" refers to an abstract idea or notion that represents a unit of thought. In SKOS, concepts are part of a controlled vocabulary or knowledge organization system, and they are used to denote a specific idea or meaning within a particular domain.

Key points about concepts in SKOS:

1. **Abstraction:** Concepts in SKOS are abstract entities that represent ideas or meanings. They are not limited to concrete objects but can encompass a wide range of intellectual or linguistic expressions.

2. **Labeling:** Each concept is associated with one or more labels that serve as human-readable identifiers. Labels can include preferred labels (e.g., preferred terms), alternative labels, and hidden labels.

3. **Notation:** Concepts can be assigned notations to provide additional identifiers or codes. Notations are often used to support interoperability and integration with other systems.

4. **Relationships:** Concepts can be related to each other through various types of relationships. SKOS provides properties like `skos:broader` and `skos:narrower` to express hierarchical relationships, as well as properties like `skos:related` to indicate associative relationships.

5. **Example:** In a concept scheme related to the animal kingdom, individual concepts might represent specific species (e.g., "Lion," "Elephant") with hierarchical relationships indicating taxonomic classifications.

In SKOS, the main elements related to concepts are:

- **skos:Concept:** The SKOS vocabulary includes the concept class, represented by the URI (Uniform Resource Identifier) `http://www.w3.org/2004/02/skos/core#Concept`. Instances of this class represent concepts.

- **skos:prefLabel:** This property is used to associate a preferred human-readable label with a concept. It represents the preferred term or label for the concept.

- **skos:altLabel:** This property is used to associate alternative human-readable labels with a concept. Alternative labels provide additional ways to refer to the same concept.

- **skos:notation:** This property is used to associate notations or codes with a concept. Notations are often used for machine processing and interoperability.

Here's a simple example in Turtle syntax:

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://example.org/Concept1>
  a skos:Concept ;
  skos:prefLabel "Lion"@en ;
  skos:altLabel "Panthera leo"@en ;
  skos:notation "A1" .
```

In this example, `<http://example.org/Concept1>` represents a concept for a lion. The concept has a preferred label ("Lion"), an alternative label ("Panthera leo"), and a notation ("A1").
