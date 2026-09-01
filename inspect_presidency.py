from pathlib import Path
from bs4 import BeautifulSoup

html = Path(
    "input/raw_html/presidency.html"
).read_text(encoding="utf-8")

soup = BeautifulSoup(html, "lxml")

print("\n========== LINKS ==========\n")

seen = set()

for link in soup.find_all("a", href=True):

    text = link.get_text(" ", strip=True)

    href = link["href"]

    if not text:
        continue

    if href in seen:
        continue

    seen.add(href)

    print(f"{text}\n -> {href}\n")