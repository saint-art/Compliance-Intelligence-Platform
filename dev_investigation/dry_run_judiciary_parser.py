from models.source_document import SourceDocument
from parsers.judiciary_parser import JudiciaryParser

parser = JudiciaryParser()

doc = SourceDocument(
    source_name="Court of Appeal",
    source_type="HTML",
    source_url="https://judiciary.go.ke/court-of-appeal-judges/",
    title="coa_judges",
    document_type="HTML",
    raw_path="input/raw_html/coa_judges_inspect.html",
    checksum="dryrun"
)
doc.document_id = "dryrun"

result = parser.parse(doc)

print(f"\nTotal judges extracted: {len(result.persons)}\n")
for p, pos in zip(result.persons, result.relationships):
    print(f"{p.full_name!r:45}")
