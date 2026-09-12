from pathlib import Path

from bs4 import BeautifulSoup


HTML_PATH = Path("input/raw_html/national_assembly_1.html")


html = HTML_PATH.read_text(
    encoding="utf-8",
    errors="ignore"
)

soup = BeautifulSoup(html, "html.parser")


print("=" * 80)
print("PAGE TITLE")
print("=" * 80)

print(soup.title.get_text(" ", strip=True) if soup.title else "NO TITLE")


print()
print("=" * 80)
print("TABLES")
print("=" * 80)

tables = soup.find_all("table")

print(f"Number of tables: {len(tables)}")

for table_index, table in enumerate(tables, start=1):

    print()
    print(f"--- TABLE {table_index} ---")

    headers = [
        cell.get_text(" ", strip=True)
        for cell in table.find_all(["th", "td"])
    ]

    print("First 50 cells:")

    for cell in headers[:50]:
        print(repr(cell))


print()
print("=" * 80)
print("LINKS CONTAINING 'MORE'")
print("=" * 80)

more_links = []

for link in soup.find_all("a", href=True):

    text = link.get_text(" ", strip=True)

    if "more" in text.lower():
        more_links.append(link)

print(f"Found: {len(more_links)}")

for link in more_links[:20]:

    print()
    print("TEXT:", repr(link.get_text(" ", strip=True)))
    print("HREF:", link.get("href"))


print()
print("=" * 80)
print("MP / MEMBER TEXT")
print("=" * 80)

keywords = [
    "Member of Parliament",
    "Constituency",
    "County",
    "Party",
    "Status",
]

for keyword in keywords:

    matches = soup.find_all(
        string=lambda value: (
            value and keyword.lower() in value.lower()
        )
    )

    print()
    print(f"{keyword}: {len(matches)} match(es)")

    for match in matches[:10]:

        parent = match.parent

        print(
            parent.name,
            repr(parent.get_text(" ", strip=True))
        )


print()
print("=" * 80)
print("LARGE CONTAINERS")
print("=" * 80)

for element in soup.find_all(["div", "section", "article"]):

    text = element.get_text(" ", strip=True)

    if "Member of Parliament" in text:

        classes = element.get("class", [])

        print()
        print("TAG:", element.name)
        print("CLASS:", classes)
        print("TEXT:", text[:1000])
        print("-" * 80)