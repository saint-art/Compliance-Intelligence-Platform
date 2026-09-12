echo "=== config.py ==="
cat config.py
echo ""
echo "=== config/ folder ==="
ls -la config/
echo ""
echo "=== database/ ==="
ls -la database/
echo ""
echo "=== collectors/ ==="
ls -la collectors/
echo ""
echo "=== models/ ==="
ls -la models/
echo ""
echo "=== pipeline/ ==="
ls -la pipeline/
echo ""
echo "=== Presidency-related files ==="
find . -iname "*presidency*" -not -path "./venv/*"
echo ""
echo "=== docs/ ==="
ls -la docs/
echo ""
echo "=== Existing DB files, if any ==="
find . -iname "*.db" -o -iname "*.sqlite" -o -iname "*.sqlite3" | grep -v venv
