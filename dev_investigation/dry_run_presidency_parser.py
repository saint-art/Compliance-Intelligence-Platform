from models.source_document import SourceDocument
from parsers.presidency_parser import PresidencyParser

parser = PresidencyParser()

test_docs = [
    SourceDocument(
        source_name="Presidency",
        source_type="HTML",
        source_url="https://www.president.go.ke/administration/office-of-the-president/",
        title="office_of_the_president",
        document_type="HTML",
        raw_path="input/raw_html/office_of_the_president_inspect.html",
        checksum="dryrun1"
    ),
    SourceDocument(
        source_name="Presidency",
        source_type="HTML",
        source_url="https://deputypresident.go.ke/leadership",
        title="dp_leadership",
        document_type="HTML",
        raw_path="input/raw_html/dp_leadership_inspect.html",
        checksum="dryrun2"
    ),
]

for doc in test_docs:
    doc.document_id = "dryrun"
    result = parser.parse(doc)
    print(f"\n{'='*70}\nSOURCE: {doc.source_url}\n{'='*70}")
    for p, pos in zip(result.persons, result.positions):
        print(f"  conf={p.confidence_score:5.1f}  {p.full_name!r:45} -> {pos.title}")
