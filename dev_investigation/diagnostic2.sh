echo "=== sqlite tables + row counts ==="
sqlite3 database/compliance.db ".tables"
echo "---"
for t in $(sqlite3 database/compliance.db ".tables"); do
  echo "$t: $(sqlite3 database/compliance.db "SELECT COUNT(*) FROM $t;") rows"
done

echo ""
echo "=== config/sources.py ==="
cat config/sources.py

echo ""
echo "=== collectors/presidency_collector.py ==="
cat collectors/presidency_collector.py

echo ""
echo "=== parsers/presidency_parser.py ==="
cat parsers/presidency_parser.py

echo ""
echo "=== Does anything import root config.py? ==="
grep -rn "import config" --include="*.py" . | grep -v venv

echo ""
echo "=== pytest baseline ==="
pytest -v 2>&1 | tail -60
