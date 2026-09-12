from models.source_document import SourceDocument
from parsers.judiciary_parser import JudiciaryParser

parser = JudiciaryParser()

doc = SourceDocument(
    source_name='Court of Appeal',
    source_type='HTML',
    source_url='https://judiciary.go.ke/court-of-appeal-judges/',
    title='coa_judges',
    document_type='HTML',
    raw_path='input/raw_html/coa_judges_inspect.html',
    checksum='dryrun'
)
doc.document_id = 'dryrun'

result = parser.parse(doc)

print('Institutions:', [i.institution_name for i in result.institutions])
print('Positions:', [p.title for p in result.positions])
print()
for r in result.relationships[:5]:
    print(f"{r.person.full_name!r:45} -> position={r.position.title!r} institution={r.institution.institution_name!r}")
