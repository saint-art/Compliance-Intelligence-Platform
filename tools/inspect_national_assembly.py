from pathlib import Path
from bs4 import BeautifulSoup

html = Path("input/raw_html/national_assembly_1.html").read_text(
    encoding="utf-8",
    errors="ignore"
)

soup = BeautifulSoup(html, "html.parser")

print("=" * 80)
print("ALL H2 HEADINGS")
print("=" * 80)

for h2 in soup.find_all("h2"):
    print(h2.get_text(" ", strip=True))

print()

print("=" * 80)
print("ALL H3 HEADINGS")
print("=" * 80)

for h3 in soup.find_all("h3"):
    print(h3.get_text(" ", strip=True))

print()

print("=" * 80)
print("ALL H4 HEADINGS")
print("=" * 80)

for h4 in soup.find_all("h4"):
    print(h4.get_text(" ", strip=True))

print()

print("=" * 80)
print("ALL IMG ALT TEXT")
print("=" * 80)

for img in soup.find_all("img")[:50]:
    print(img.get("alt"))
    print(img.get("src"))
    print("-" * 40)