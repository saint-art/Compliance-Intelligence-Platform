from database.database_manager import DatabaseManager

from loaders.person_repository import PersonRepository
from loaders.position_repository import PositionRepository
from loaders.institution_repository import InstitutionRepository
from loaders.person_position_repository import PersonPositionRepository
from loaders.source_repository import SourceRepository

from resolvers.relationship_resolver import RelationshipResolver

from models.source import Source


class PersistenceService:

    def __init__(self, connection=None):

        self._owns_connection = connection is None

        if connection is None:
            self.connection = DatabaseManager.connect()
        else:
            self.connection = connection

        self.person_repository = PersonRepository(
            self.connection
        )

        self.position_repository = PositionRepository(
            self.connection
        )

        self.institution_repository = InstitutionRepository(
            self.connection
        )

        self.person_position_repository = (
            PersonPositionRepository(
                self.connection
            )
        )

        self.source_repository = SourceRepository(
            self.connection
        )

        self.relationship_resolver = (
            RelationshipResolver()
        )

    def _get_source_document_url(self, document_id, cache):
        """
        Look up a source_document's URL by its document_id,
        caching results within this persist() call so a batch
        of relationships sharing the same document only costs
        one query.
        """

        if document_id in cache:
            return cache[document_id]

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT source_url FROM source_documents "
            "WHERE document_id = ?",
            (document_id,)
        )

        row = cursor.fetchone()

        url = row["source_url"] if row else ""

        cache[document_id] = url

        return url

    def persist(self, parser_result):

        try:

            for institution in parser_result.institutions:

                self.institution_repository.save(
                    institution
                )

            for position in parser_result.positions:

                self.position_repository.save(
                    position
                )

            for person in parser_result.persons:

                self.person_repository.save(
                    person
                )

            relationships = (
                self.relationship_resolver.resolve(
                    parser_result
                )
            )

            relationship_count = 0
            document_url_cache = {}

            for relationship in relationships:

                self.person_position_repository.save(
                    relationship
                )

                relationship_count += 1

                source_url = self._get_source_document_url(
                    relationship.source_document_id,
                    document_url_cache
                )

                citation = Source(
                    person_id=relationship.person_id,
                    source_name=relationship.person.primary_source or "",
                    source_url=source_url,
                    source_type="HTML",
                    trust_score=relationship.person.confidence_score
                )

                self.source_repository.save(citation)

            if self._owns_connection:
                self.connection.commit()

            return {
                "persons": len(
                    parser_result.persons
                ),
                "positions": len(
                    parser_result.positions
                ),
                "institutions": len(
                    parser_result.institutions
                ),
                "relationships": relationship_count
            }

        except Exception:

            if self._owns_connection:
                self.connection.rollback()

            raise

    def close(self):

        if (
            self.connection is not None
            and self._owns_connection
        ):

            self.connection.close()

        self.connection = None
