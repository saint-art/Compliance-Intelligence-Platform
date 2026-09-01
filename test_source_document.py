from database.database_manager import DatabaseManager
from loaders.source_document_repository import SourceDocumentRepository
from models.source_document import SourceDocument


def main():

    DatabaseManager.connect()

    repository = SourceDocumentRepository()

    document = SourceDocument(
        source_name="Presidency",
        source_type="HTML",
        source_url="https://www.president.go.ke/",
        title="Presidency Homepage",
        document_type="HTML",
        raw_path="input/raw_html/presidency.html",
        checksum="test_checksum_001"
    )

    repository.save(document)

    print("\nSaved SourceDocument\n")
    print(document)


if __name__ == "__main__":
    main()