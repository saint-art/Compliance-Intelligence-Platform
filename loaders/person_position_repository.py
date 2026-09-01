from loaders.base_repository import BaseRepository
from models.person_position import PersonPosition


class PersonPositionRepository(BaseRepository):

    def __init__(self, connection=None):
        super().__init__(connection)

    def relationship_exists(
        self,
        relationship
    ):
        self.cursor.execute(
            """
            SELECT
                person_position_id,
                source_document_id
            FROM person_positions
            WHERE person_id = ?
            AND position_id = ?
            AND institution_id = ?
            LIMIT 1
            """,
            (
                relationship.person_id,
                relationship.position_id,
                relationship.institution_id
            )
        )
        return self.cursor.fetchone()

    def save(
        self,
        relationship: PersonPosition
    ):
        if relationship.person_id is None:
            raise ValueError(
                "PersonPosition missing person_id."
            )

        if relationship.position_id is None:
            raise ValueError(
                "PersonPosition missing position_id."
            )

        if relationship.institution_id is None:
            raise ValueError(
                "PersonPosition missing institution_id."
            )

        existing = self.relationship_exists(
            relationship
        )

        # -----------------------------------------------------
        # EXISTING RELATIONSHIP
        # -----------------------------------------------------

        if existing:
            existing_id = existing[
                "person_position_id"
            ]

            existing_source_id = existing[
                "source_document_id"
            ]

            new_source_id = (
                relationship.source_document_id
            )

            # -------------------------------------------------
            # UPDATE PROVENANCE WHEN A NEW SOURCE DOCUMENT
            # IS AVAILABLE.
            # -------------------------------------------------

            if (
                new_source_id
                and existing_source_id != new_source_id
            ):
                self.cursor.execute(
                    """
                    UPDATE person_positions
                    SET
                        source_document_id = ?,
                        start_date = ?,
                        end_date = ?,
                        is_current = ?,
                        confidence_score = ?,
                        updated_at = ?
                    WHERE person_position_id = ?
                    """,
                    (
                        new_source_id,
                        relationship.start_date,
                        relationship.end_date,
                        int(relationship.is_current),
                        relationship.confidence_score,
                        relationship.updated_at,
                        existing_id
                    )
                )

                self.logger.info(
                    "Updated relationship provenance."
                )

            else:
                self.logger.info(
                    "Relationship already exists."
                )

            return existing_id

        # -----------------------------------------------------
        # NEW RELATIONSHIP
        # -----------------------------------------------------

        self.cursor.execute(
            """
            INSERT INTO person_positions(
                person_position_id,
                person_id,
                position_id,
                institution_id,
                source_document_id,
                start_date,
                end_date,
                is_current,
                confidence_score,
                created_at,
                updated_at
            )
            VALUES(
                ?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                relationship.person_position_id,
                relationship.person_id,
                relationship.position_id,
                relationship.institution_id,
                relationship.source_document_id,
                relationship.start_date,
                relationship.end_date,
                int(relationship.is_current),
                relationship.confidence_score,
                relationship.created_at,
                relationship.updated_at
            )
        )

        self.logger.info(
            "Inserted PersonPosition relationship."
        )

        return relationship.person_position_id

    def save_many(
        self,
        relationships
    ):
        ids = []

        for relationship in relationships:
            ids.append(
                self.save(relationship)
            )

        return ids
