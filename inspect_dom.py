from pathlib import Path
from bs4 import BeautifulSoup

html = Path(
    "input/raw_html/cabinet.html"
).read_text(encoding="utf-8")

soup = BeautifulSoup(html, "lxml")

cards = soup.select(".repeater-item")

print(f"\nFound {len(cards)} repeater items\n")

for i, card in enumerate(cards, 1):

    print("=" * 80)

    print(f"CARD {i}")

    print("=" * 80)

    print(card.get_text("\n", strip=True)[:2000])

    print()