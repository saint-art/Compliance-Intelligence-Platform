echo "=== All persons currently in DB ==="
sqlite3 database/compliance.db -header -column "SELECT id, full_name, is_pep, confidence_score, primary_source FROM persons;"

echo ""
echo "=== Positions ==="
sqlite3 database/compliance.db -header -column "SELECT id, title, category FROM positions;"

echo ""
echo "=== cabinet_collector.py ==="
cat collectors/cabinet_collector.py

echo ""
echo "=== cabinet parser file (find it) ==="
find . -iname "*cabinet_parser*" -not -path "./venv/*" -not -path "./tests/*" | xargs -I{} echo {}
find . -iname "*cabinet_parser*" -not -path "./venv/*" -not -path "*test*"

echo ""
echo "=== schema.sql ==="
cat database/schema.sql
