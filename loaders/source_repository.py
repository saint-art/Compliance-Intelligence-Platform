from loaders.base_repository import BaseRepository
from models.source import Source
from utils.logger import get_logger


class SourceRepository(BaseRepository):
    """
    Persists citation records to the `sources` table.

    Unlike PersonRepository/PositionRepository, this is
    append-only by design: a person can legitimately have
    multiple citation rows over time (e.g. re-verified on a
    later date, or corroborated by a second source), so save()
    always inserts rather than upserting.
    """

    def __init__(self, connection=None):
        super().__init__(connection=connection)
        self.cursor = self.connection.cursor()
        self.logger = get_logger("SourceRepository")

    def save(self, source: Source):

        self.cursor.execute(
            """
            INSERT INTO sources (

                person_id,
                source_name,
                source_url,
                source_type,
                trust_score,
                collected_at,
                last_verified

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source.person_id,
                source.source_name,
                source.source_url,
                source.source_type,
                source.trust_score,
                source.collected_at,
                source.last_verified
            )
        )

        source.source_id = self.cursor.lastrowid

        self.logger.info(
            f"Inserted source citation for person_id="
            f"{source.person_id} -> {source.source_url}"
        )

        return source.source_id

    def save_many(self, sources):

        ids = []

        for source in sources:
            ids.append(self.save(source))

        return ids
