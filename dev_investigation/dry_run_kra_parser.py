from models.source_document import SourceDocument
from parsers.kra_parser import KRAParser

parser = KRAParser()

doc = SourceDocument(
    source_name="Kenya Revenue Authority",
    source_type="HTML",
    source_url="https://www.kra.go.ke/about-kra/leadership",
    title="kra_leadership",
    document_type="HTML",
    raw_path="input/raw_html/kra_leadership_inspect.html",
    checksum="dryrun"
)
doc.document_id = "dryrun"

result = parser.parse(doc)

print(f"\nTotal extracted: {len(result.persons)}\n")
for p, r in zip(result.persons, result.relationships):
    print(f"{p.full_name!r:40} -> {r.position.title}")
