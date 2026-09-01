from pathlib import Path
from bs4 import BeautifulSoup

RAW_HTML = Path("input/raw_html")

for file in sorted(RAW_HTML.glob("*.html")):

    print("\n" + "=" * 80)
    print(file.name)
    print("=" * 80)

    soup = BeautifulSoup(
        file.read_text(encoding="utf-8"),
        "lxml"
    )

    title = soup.title.get_text(strip=True) if soup.title else "No title"

    print(f"TITLE: {title}")

    print("\nHEADINGS\n")

    headings = soup.find_all(["h1", "h2", "h3"])

    for heading in headings[:15]:

        text = heading.get_text(" ", strip=True)

        if text:

            print("-", text)