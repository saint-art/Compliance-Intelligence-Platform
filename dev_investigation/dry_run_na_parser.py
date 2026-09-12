from models.source_document import SourceDocument
from parsers.national_assembly_parser import NationalAssemblyParser

parser = NationalAssemblyParser()

doc = SourceDocument(
    source_name="National Assembly",
    source_type="HTML",
    source_url="https://www.parliament.go.ke/the-national-assembly/mps",
    title="national_assembly_1",
    document_type="HTML",
    raw_path="input/raw_html/national_assembly_1.html",
    checksum="dryrun"
)
doc.document_id = "dryrun"

result = parser.parse(doc)

print(f"\nTotal MPs extracted: {len(result.persons)}\n")
for p in result.persons[:10]:
    print(f"{p.full_name!r:45} county={p.county!r:12} constituency={p.constituency!r:15} party={p.party if hasattr(p,'party') else p.political_party!r}")
