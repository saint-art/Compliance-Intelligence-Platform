from models.source_document import SourceDocument
from parsers.senate_parser import SenateParser
from pathlib import Path

# Find the page 1 snapshot we just saved
snapshot = sorted(Path("input/raw_html").glob("senate_1_*.html"))[0]

parser = SenateParser()

doc = SourceDocument(
    source_name="Senate",
    source_type="HTML",
    source_url="https://www.parliament.go.ke/the-senate/senators",
    title="senate_1",
    document_type="HTML",
    raw_path=str(snapshot),
    checksum="dryrun"
)
doc.document_id = "dryrun"

result = parser.parse(doc)

print(f"\nTotal senators extracted: {len(result.persons)}\n")
for p in result.persons:
    print(f"{p.full_name!r:45} county={p.county!r:12} party={p.political_party!r}")
