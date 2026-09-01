from typing import List

from database.database_manager import DatabaseManager
from loaders.base_repository import BaseRepository
from models.source_run import SourceRun
from utils.logger import get_logger


class SourceRunRepository(BaseRepository):
    """
    Repository for SourceRun persistence.

    SourceRun records represent execution metadata for a single
    collector/source ingestion run.

    Transaction ownership belongs to the caller.

    Therefore this repository NEVER commits automatically after
    save() or update().
    """

    def __init__(self, connection=None):

        super().__init__(
            connection=connection
        )

        self.logger = get_logger(
            "SourceRunRepository"
        )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def save(self, run: SourceRun):

        self.cursor.execute(
            """
            INSERT INTO source_runs
            (
                collector_name,
                source_name,
                records_found,
                inserted,
                updated,
                skipped,
                started_at,
                finished_at,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run.collector_name,
                run.source_name,
                run.records_found,
                run.inserted,
                run.updated,
                run.skipped,
                run.started_at,
                run.finished_at,
                run.status
            )
        )

        run.run_id = self.cursor.lastrowid

        self.logger.info(
            f"Created SourceRun {run.run_id}"
        )

        return run

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self, run: SourceRun):

        if run.run_id is None:

            raise ValueError(
                "Cannot update SourceRun without run_id."
            )

        self.cursor.execute(
            """
            UPDATE source_runs

            SET
                collector_name = ?,
                source_name = ?,
                records_found = ?,
                inserted = ?,
                updated = ?,
                skipped = ?,
                started_at = ?,
                finished_at = ?,
                status = ?

            WHERE run_id = ?
            """,
            (
                run.collector_name,
                run.source_name,
                run.records_found,
                run.inserted,
                run.updated,
                run.skipped,
                run.started_at,
                run.finished_at,
                run.status,
                run.run_id
            )
        )

        updated = self.cursor.rowcount > 0

        if updated:

            self.logger.info(
                f"Updated SourceRun {run.run_id}"
            )

        else:

            self.logger.warning(
                f"SourceRun not found: {run.run_id}"
            )

        return updated

    # ---------------------------------------------------------
    # FINISH
    # ---------------------------------------------------------

    def finish(self, run: SourceRun):

        if run.run_id is None:

            raise ValueError(
                "Cannot finish SourceRun without run_id."
            )

        run.finish()

        self.update(run)

        return run

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    def get(self, run_id: int):

        self.cursor.execute(
            """
            SELECT *
            FROM source_runs
            WHERE run_id = ?
            """,
            (run_id,)
        )

        return self.cursor.fetchone()

    # ---------------------------------------------------------
    # BULK
    # ---------------------------------------------------------

    def save_many(
        self,
        entities: List[SourceRun]
    ):

        return [
            self.save(entity)
            for entity in entities
        ]