from typing import List, Optional

from loaders.base_repository import BaseRepository
from models.source_document import SourceDocument


class SourceDocumentRepository(BaseRepository):
    """
    Repository for SourceDocument persistence.

    Responsible for:

    - saving collected documents
    - duplicate detection
    - retrieving documents
    - updating metadata
    - deleting documents
    """

    def __init__(self, connection=None):
        super().__init__(connection=connection)

    # ---------------------------------------------------------
    # INTERNAL MAPPING
    # ---------------------------------------------------------

    def _row_to_document(self, row) -> Optional[SourceDocument]:

        if row is None:
            return None

        return SourceDocument(

            document_id=row["document_id"],
            source_name=row["source_name"],
            source_type=row["source_type"],
            source_url=row["source_url"],
            external_id=row["external_id"],
            title=row["title"],
            document_type=row["document_type"],
            published_at=row["published_at"],
            modified_at=row["modified_at"],
            collected_at=row["collected_at"],
            raw_path=row["raw_path"],
            checksum=row["checksum"],
            status=row["status"]

        )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def save(self, document: SourceDocument) -> str:

        existing = self.get_by_checksum(
            document.checksum
        )

        if existing:

            document.document_id = existing.document_id

            self.logger.info(
                f"Document already exists: "
                f"{document.title} "
                f"(ID {existing.document_id})"
            )

            return existing.document_id

        self.cursor.execute(
            """
            INSERT INTO source_documents (

                document_id,
                source_name,
                source_type,
                source_url,
                external_id,
                title,
                document_type,
                published_at,
                modified_at,
                collected_at,
                raw_path,
                checksum,
                status

            )

            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                document.document_id,
                document.source_name,
                document.source_type,
                document.source_url,
                document.external_id,
                document.title,
                document.document_type,
                document.published_at,
                document.modified_at,
                document.collected_at,
                document.raw_path,
                document.checksum,
                document.status
            )
        )

        self.logger.info(
            f"Saved document "
            f"{document.title} "
            f"(ID {document.document_id})"
        )

        return document.document_id

    # ---------------------------------------------------------
    # BULK INSERT
    # ---------------------------------------------------------

    def save_many(
        self,
        documents: List[SourceDocument]
    ) -> List[str]:

        return [
            self.save(document)
            for document in documents
        ]

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    def get(
        self,
        document_id: str
    ) -> Optional[SourceDocument]:

        self.cursor.execute(
            """
            SELECT *

            FROM source_documents

            WHERE document_id = ?
            """,
            (document_id,)
        )

        return self._row_to_document(
            self.cursor.fetchone()
        )

    # ---------------------------------------------------------
    # DUPLICATE DETECTION
    # ---------------------------------------------------------

    def exists(
        self,
        checksum: str
    ) -> bool:

        return self.get_by_checksum(checksum) is not None

    def get_by_checksum(
        self,
        checksum: str
    ) -> Optional[SourceDocument]:

        if not checksum:
            return None

        self.cursor.execute(
            """
            SELECT *

            FROM source_documents

            WHERE checksum = ?

            LIMIT 1
            """,
            (checksum,)
        )

        return self._row_to_document(
            self.cursor.fetchone()
        )

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(
        self,
        document: SourceDocument
    ) -> bool:

        self.cursor.execute(
            """
            UPDATE source_documents

            SET

                source_name = ?,
                source_type = ?,
                source_url = ?,
                external_id = ?,
                title = ?,
                document_type = ?,
                published_at = ?,
                modified_at = ?,
                collected_at = ?,
                raw_path = ?,
                checksum = ?,
                status = ?

            WHERE document_id = ?
            """,
            (
                document.source_name,
                document.source_type,
                document.source_url,
                document.external_id,
                document.title,
                document.document_type,
                document.published_at,
                document.modified_at,
                document.collected_at,
                document.raw_path,
                document.checksum,
                document.status,
                document.document_id
            )
        )

        updated = self.cursor.rowcount > 0

        if updated:

            self.logger.info(
                f"Updated document "
                f"{document.title} "
                f"(ID {document.document_id})"
            )

        else:

            self.logger.warning(
                f"Document not found for update: "
                f"{document.document_id}"
            )

        return updated

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(
        self,
        document_id: str
    ) -> bool:

        self.cursor.execute(
            """
            DELETE

            FROM source_documents

            WHERE document_id = ?
            """,
            (document_id,)
        )

        deleted = self.cursor.rowcount > 0

        if deleted:

            self.logger.info(
                f"Deleted document {document_id}"
            )

        else:

            self.logger.warning(
                f"Document not found for deletion: "
                f"{document_id}"
            )

        return deleted