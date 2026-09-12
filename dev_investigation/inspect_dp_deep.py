from bs4 import BeautifulSoup
from pathlib import Path

html = Path("input/raw_html/dp_leadership_inspect.html").read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "lxml")

container = soup.find("div", class_="field--name-field-content-builder")

print("="*70)
print("Direct children of the content-builder field")
print("="*70)

for child in container.find_all(recursive=False):
    print(f"\n<{child.name} class={child.get('class')}>")

print("\n" + "="*70)
print("All elements inside container with an 'id' attribute")
print("="*70)
for el in container.find_all(id=True):
    print(f"<{el.name} id='{el.get('id')}' class={el.get('class')}> {el.get_text(' ', strip=True)[:100]}")

print("\n" + "="*70)
print("Every div at any depth inside container, with class + short text")
print("="*70)
for div in container.find_all("div"):
    classes = div.get("class")
    text = div.get_text(" ", strip=True)
    if text and len(text) < 120:
        print(f"<div class={classes}> {text}")

print("\n" + "="*70)
print("Images inside container (often one per person)")
print("="*70)
for img in container.find_all("img"):
    print(f"alt='{img.get('alt')}' src={img.get('src') or img.get('data-src')}")
