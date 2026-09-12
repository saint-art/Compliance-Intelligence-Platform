from bs4 import BeautifulSoup
from pathlib import Path

html = Path("input/raw_html/dp_leadership_inspect.html").read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "lxml")

cards = soup.find_all("div", class_="gsc-column")
print(f"Found {len(cards)} gsc-column cards\n")

for i, card in enumerate(cards, 1):
    desc = card.find("div", class_="desc")
    print(f"--- CARD {i} ---")
    if desc:
        print(desc.prettify()[:800])
    print()
