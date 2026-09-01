from database.database_manager import DatabaseManager

from loaders.person_repository import PersonRepository
from loaders.position_repository import PositionRepository
from loaders.institution_repository import InstitutionRepository
from loaders.person_position_repository import PersonPositionRepository

from resolvers.relationship_resolver import RelationshipResolver


class PersistenceService:

    def __init__(self, connection=None):

        # -----------------------------------------------------
        # DATABASE CONNECTION
        # -----------------------------------------------------
        #
        # If a connection is supplied by the caller, this
        # service participates in the caller's transaction.
        #
        # Otherwise, the service creates its own connection
        # for standalone use.
        #
        # -----------------------------------------------------

        self._owns_connection = connection is None

        if connection is None:
            self.connection = DatabaseManager.connect()
        else:
            self.connection = connection

        # -----------------------------------------------------
        # SHARED REPOSITORIES
        # -----------------------------------------------------
        #
        # Every repository operates on the same connection.
        #
        # -----------------------------------------------------

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

        self.relationship_resolver = (
            RelationshipResolver()
        )

    def persist(self, parser_result):

        try:

            # -------------------------------------------------
            # INSTITUTIONS
            # -------------------------------------------------

            for institution in parser_result.institutions:

                self.institution_repository.save(
                    institution
                )

            # -------------------------------------------------
            # POSITIONS
            # -------------------------------------------------

            for position in parser_result.positions:

                self.position_repository.save(
                    position
                )

            # -------------------------------------------------
            # PERSONS
            # -------------------------------------------------

            for person in parser_result.persons:

                self.person_repository.save(
                    person
                )

            # -------------------------------------------------
            # RELATIONSHIPS
            # -------------------------------------------------

            relationships = (
                self.relationship_resolver.resolve(
                    parser_result
                )
            )

            relationship_count = 0

            for relationship in relationships:

                self.person_position_repository.save(
                    relationship
                )

                relationship_count += 1

            # -------------------------------------------------
            # COMMIT
            # -------------------------------------------------
            #
            # The caller owns the transaction when a connection
            # was injected.
            #
            # Therefore, only commit when this service created
            # the connection itself.
            #
            # -------------------------------------------------

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

            # -------------------------------------------------
            # ROLLBACK
            # -------------------------------------------------
            #
            # Only rollback when this service owns the
            # transaction.
            #
            # If the connection was injected, the caller
            # controls rollback.
            #
            # -------------------------------------------------

            if self._owns_connection:
                self.connection.rollback()

            raise

    def close(self):

        # -----------------------------------------------------
        # CONNECTION OWNERSHIP
        # -----------------------------------------------------
        #
        # Never close an externally supplied connection.
        #
        # -----------------------------------------------------

        if (
            self.connection is not None
            and self._owns_connection
        ):

            self.connection.close()

        self.connection = None