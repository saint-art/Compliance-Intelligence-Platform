from models.source_document import SourceDocument
from parsers.governors_parser import GovernorsParser

parser = GovernorsParser()

doc = SourceDocument(
    source_name="Governors",
    source_type="HTML",
    source_url="https://cog.go.ke/current-governors/",
    title="governors",
    document_type="HTML",
    raw_path="input/raw_html/governors_inspect.html",
    checksum="dryrun"
)
doc.document_id = "dryrun"

result = parser.parse(doc)

print(f"\nTotal governors extracted: {len(result.persons)}\n")
for p in result.persons:
    print(f"{p.full_name!r:45} county={p.county!r}")
