class RelationshipResolver:

    """
    Resolves object references into database foreign-key IDs.

    All relationship provenance must already be present on the
    relationship itself.
    """

    def resolve(self, parser_result):

        resolved = []

        for relationship in parser_result.relationships:

            if relationship.person is not None:

                if relationship.person.person_id is None:

                    raise ValueError(
                        "Unable to resolve relationship: "
                        f"person '{relationship.person.full_name}' "
                        "has no database person_id."
                    )

                relationship.person_id = (
                    relationship.person.person_id
                )

            if relationship.position is not None:

                if relationship.position.position_id is None:

                    raise ValueError(
                        "Unable to resolve relationship: "
                        f"position '{relationship.position.title}' "
                        "has no database position_id."
                    )

                relationship.position_id = (
                    relationship.position.position_id
                )

            if relationship.institution is not None:

                if (
                    relationship.institution.institution_id
                    is None
                ):

                    raise ValueError(
                        "Unable to resolve relationship: "
                        f"institution "
                        f"'{relationship.institution.institution_name}' "
                        "has no database institution_id."
                    )

                relationship.institution_id = (
                    relationship.institution.institution_id
                )

            relationship.validate()

            resolved.append(
                relationship
            )

        return resolved