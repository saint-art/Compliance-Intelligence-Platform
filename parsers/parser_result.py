from dataclasses import dataclass, field


@dataclass
class ParserResult:
    """
    Result produced by a parser for one or more source documents.

    A single parser invocation should normally contain one
    source_document.

    A merged ParserResult may contain entities and relationships
    originating from multiple source documents. Relationship
    provenance must therefore be stored directly on each relationship.
    """

    source_document: object = None

    persons: list = field(default_factory=list)
    institutions: list = field(default_factory=list)
    positions: list = field(default_factory=list)
    organisations: list = field(default_factory=list)
    companies: list = field(default_factory=list)
    sanctions: list = field(default_factory=list)
    addresses: list = field(default_factory=list)
    identifiers: list = field(default_factory=list)

    relationships: list = field(default_factory=list)

    person_positions: list = field(default_factory=list)
    person_organisations: list = field(default_factory=list)
    person_companies: list = field(default_factory=list)
    person_addresses: list = field(default_factory=list)
    aliases: list = field(default_factory=list)

    def merge(self, other: "ParserResult"):

        if not isinstance(other, ParserResult):
            raise TypeError(
                "ParserResult.merge() expects another ParserResult."
            )

        self.persons.extend(other.persons)
        self.institutions.extend(other.institutions)
        self.positions.extend(other.positions)

        self.organisations.extend(
            other.organisations
        )

        self.companies.extend(
            other.companies
        )

        self.sanctions.extend(
            other.sanctions
        )

        self.addresses.extend(
            other.addresses
        )

        self.identifiers.extend(
            other.identifiers
        )

        self.relationships.extend(
            other.relationships
        )

        self.person_positions.extend(
            other.person_positions
        )

        self.person_organisations.extend(
            other.person_organisations
        )

        self.person_companies.extend(
            other.person_companies
        )

        self.person_addresses.extend(
            other.person_addresses
        )

        self.aliases.extend(
            other.aliases
        )

    @property
    def extracted_count(self):

        return (
            len(self.persons)
            + len(self.institutions)
            + len(self.positions)
            + len(self.organisations)
            + len(self.companies)
            + len(self.sanctions)
            + len(self.addresses)
            + len(self.identifiers)
        )

    @property
    def relationship_count(self):

        return len(self.relationships)

    @property
    def total_objects(self):

        return (
            self.extracted_count
            + self.relationship_count
        )