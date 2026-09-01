from bs4 import BeautifulSoup

html = open(
    "input/raw_html/cabinet.html",
    encoding="utf-8"
).read()

soup = BeautifulSoup(html, "html.parser")

print("=" * 80)
print("TITLE")
print("=" * 80)
print(soup.title)

print()

print("=" * 80)
print("HEADINGS")
print("=" * 80)

for h in soup.find_all(["h1","h2","h3","h4"])[:50]:
    print(h.get_text(" ", strip=True))

print()

print("=" * 80)
print("FIRST 100 LINKS")
print("=" * 80)

for a in soup.find_all("a", href=True)[:100]:
    print(a.get_text(" ", strip=True))
    print(a["href"])
    print("-" * 40)

print()

print("=" * 80)
print("FIRST 100 CLASSES")
print("=" * 80)

classes = set()

for tag in soup.find_all(True):
    cls = tag.get("class")
    if cls:
        classes.add(" ".join(cls))

for c in sorted(classes)[:100]:
    print(c)