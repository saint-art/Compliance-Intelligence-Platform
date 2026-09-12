from bs4 import BeautifulSoup
from pathlib import Path

html = Path("input/raw_html/national_assembly_1.html").read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

tables = soup.find_all("table")
mp_table = tables[2]  # Table 3 from the inspection output

print("=== TABLE ATTRS ===")
print(mp_table.get("class"), mp_table.get("id"))

rows = mp_table.find_all("tr")
print(f"\nTotal rows: {len(rows)}")

print("\n=== HEADER ROW (raw HTML) ===")
print(rows[0].prettify()[:1500])

print("\n=== FIRST DATA ROW (raw HTML) ===")
print(rows[1].prettify()[:1500])

print("\n=== SECOND DATA ROW (raw HTML) ===")
print(rows[2].prettify()[:1500])
