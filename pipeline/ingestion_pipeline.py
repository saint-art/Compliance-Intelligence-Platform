from database.database_manager import DatabaseManager

from pipeline.base_pipeline import BasePipeline
from pipeline.pipeline_result import PipelineResult

from utils.logger import get_logger

from models.source_run import SourceRun

from loaders.source_run_repository import SourceRunRepository
from loaders.source_document_repository import SourceDocumentRepository

from parsers.parser_result import ParserResult

from services.persistence_service import PersistenceService


class IngestionPipeline(BasePipeline):

    def __init__(
        self,
        collector,
        parser
    ):

        self.collector = collector
        self.parser = parser

        self.logger = get_logger(
            "IngestionPipeline"
        )

        # -----------------------------------------------------
        # AUDIT CONNECTION
        # -----------------------------------------------------
        #
        # SourceRun deliberately has its own connection.
        #
        # This allows a FAILED ingestion run to be committed
        # even when the main data transaction is rolled back.
        #
        # -----------------------------------------------------

        self.source_run_repository = (
            SourceRunRepository()
        )

        # -----------------------------------------------------
        # DATA CONNECTION
        # -----------------------------------------------------
        #
        # Source documents and extracted entities share one
        # transaction.
        #
        # -----------------------------------------------------

        self.connection = (
            DatabaseManager.connect()
        )

        self.source_document_repository = (
            SourceDocumentRepository(
                self.connection
            )
        )

        self.persistence_service = (
            PersistenceService(
                self.connection
            )
        )

    def run(self):

        run = SourceRun(
            collector_name=(
                self.collector.__class__.__name__
            ),
            source_name=self.collector.source_name
        )

        self.source_run_repository.save(run)
        self.source_run_repository.connection.commit()

        result = PipelineResult(
            source_name=self.collector.source_name
        )

        result.start()

        try:

            self.logger.info(
                "Starting ingestion pipeline"
            )

            # -------------------------------------------------
            # STEP 1
            # Collect documents
            # -------------------------------------------------

            collected = self.collector.collect()

            if isinstance(collected, list):
                documents = collected
            else:
                documents = [collected]

            result.documents_processed = len(
                documents
            )

            # -------------------------------------------------
            # STEP 2
            # Master ParserResult
            # -------------------------------------------------

            master = ParserResult()

            # -------------------------------------------------
            # STEP 3
            # Parse every document
            # -------------------------------------------------

            for document in documents:

                saved_document_id = (
                    self.source_document_repository.save(
                        document
                    )
                )

                document.document_id = (
                    saved_document_id
                )

                parsed = self.parser.parse(
                    document
                )

                master.merge(parsed)

            # -------------------------------------------------
            # STEP 4
            # Persist merged graph
            # -------------------------------------------------

            run.records_found = (
                master.extracted_count
            )

            result.entities_created = (
                master.extracted_count
            )

            stats = (
                self.persistence_service.persist(
                    master
                )
            )

            # -------------------------------------------------
            # STEP 5
            # COMMIT DATA TRANSACTION
            # -------------------------------------------------
            #
            # Documents, persons, positions, institutions and
            # relationships are committed together.
            #
            # -------------------------------------------------

            self.connection.commit()

            # -------------------------------------------------
            # STEP 6
            # COMPLETE AND COMMIT AUDIT RUN
            # -------------------------------------------------

            run.inserted = stats["persons"]
            run.status = "SUCCESS"

            self.source_run_repository.finish(
                run
            )

            self.source_run_repository.connection.commit()

            result.entities_saved = (
                master.extracted_count
            )

            result.success = True

            self.logger.info(
                f"Saved "
                f"{stats['persons']} persons, "
                f"{stats['positions']} positions, "
                f"{stats['institutions']} institutions and "
                f"{stats['relationships']} relationships."
            )

        except Exception as ex:

            # -------------------------------------------------
            # STEP 1
            # ROLLBACK MAIN DATA TRANSACTION
            # -------------------------------------------------

            self.connection.rollback()

            # -------------------------------------------------
            # STEP 2
            # RECORD FAILED AUDIT RUN
            # -------------------------------------------------
            #
            # The audit connection is independent, so this
            # record survives the main transaction rollback.
            #
            # -------------------------------------------------

            run.status = "FAILED"

            self.source_run_repository.finish(
                run
            )

            # -------------------------------------------------
            # STEP 3
            # COMMIT FAILED AUDIT RUN
            # -------------------------------------------------

            self.source_run_repository.connection.commit()

            result.error = str(ex)

            self.logger.exception(ex)

        finally:

            result.finish()

        return result

    def close(self):

        # -----------------------------------------------------
        # CLOSE DATA CONNECTION
        # -----------------------------------------------------

        if self.connection is not None:

            self.connection.close()

            self.connection = None

        # -----------------------------------------------------
        # CLOSE AUDIT CONNECTION
        # -----------------------------------------------------

        self.source_run_repository.close()
