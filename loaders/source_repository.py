from loaders.base_repository import BaseRepository
from models.source import Source
from utils.logger import get_logger


class SourceRepository(BaseRepository):
    """
    Persists citation records to the `sources` table.

    save() is an upsert keyed on (person_id, source_name,
    source_url): if an identical citation already exists, its
    last_verified timestamp is refreshed in place rather than
    inserting a duplicate row. This means re-running a pipeline
    against unchanged source data (e.g. via a test suite, or a
    scheduled re-check) does not silently accumulate duplicate
    citations over time.

    A genuinely new citation (different source_url, e.g. the
    person moved to a new institution) still creates a new row,
    preserving history rather than overwriting it.
    """

    def __init__(self, connection=None):
        super().__init__(connection=connection)
        self.cursor = self.connection.cursor()
        self.logger = get_logger("SourceRepository")

    def find_existing(self, source: Source):

        self.cursor.execute(
            """
            SELECT source_id
            FROM sources
            WHERE person_id = ?
            AND source_name = ?
            AND source_url = ?
            LIMIT 1
            """,
            (
                source.person_id,
                source.source_name,
                source.source_url
            )
        )

        return self.cursor.fetchone()

    def save(self, source: Source):

        existing = self.find_existing(source)

        if existing:

            existing_id = existing["source_id"]

            self.cursor.execute(
                """
                UPDATE sources
                SET last_verified = ?,
                    trust_score = ?
                WHERE source_id = ?
                """,
                (
                    source.last_verified,
                    source.trust_score,
                    existing_id
                )
            )

            source.source_id = existing_id

            self.logger.info(
                f"Citation already exists for person_id="
                f"{source.person_id} -> {source.source_url}, "
                f"refreshed last_verified."
            )

            return existing_id

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
