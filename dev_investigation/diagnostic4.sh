echo "=== Persons in DB ==="
sqlite3 database/compliance.db -header -column "SELECT person_id, full_name, is_pep, confidence_score, primary_source, political_party, county FROM persons;"

echo ""
echo "=== Positions in DB ==="
sqlite3 database/compliance.db -header -column "SELECT position_id, title, category FROM positions;"

echo ""
echo "=== Institutions in DB ==="
sqlite3 database/compliance.db -header -column "SELECT * FROM institutions;"

echo ""
echo "=== cabinet_parser.py (full) ==="
cat parsers/cabinet_parser.py
