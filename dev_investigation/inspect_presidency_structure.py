from bs4 import BeautifulSoup
from pathlib import Path
import requests

headers = {"User-Agent": "Compliance-Intelligence-Platform/1.0"}

# --- Office of the President: look at structure around each h4.brxe-heading ---
html = Path("input/raw_html/office_of_the_president_inspect.html").read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "lxml")

print("="*70)
print("OFFICE OF THE PRESIDENT — full parent structure around each heading")
print("="*70)

for h in soup.find_all("h4"):
    text = h.get_text(" ", strip=True)
    if not text:
        continue
    print(f"\n--- HEADING: {text[:80]} ---")
    parent = h.parent
    print(f"Parent tag: <{parent.name} class={parent.get('class')}>")
    # print siblings' text to find position title
    for sib in parent.find_all(recursive=True):
        t = sib.get_text(" ", strip=True)
        if t and t != text and len(t) < 200:
            print(f"  sibling <{sib.name} class={sib.get('class')}>: {t}")

# --- Deputy President site ---
print("\n\n" + "="*70)
print("FETCHING deputypresident.go.ke/leadership")
print("="*70)

resp = requests.get("https://deputypresident.go.ke/leadership", headers=headers, timeout=30)
resp.raise_for_status()
Path("input/raw_html/dp_leadership_inspect.html").write_text(resp.text, encoding="utf-8", errors="ignore")

soup2 = BeautifulSoup(resp.text, "lxml")
for h in soup2.find_all(["h1","h2","h3","h4","h5","h6"]):
    text = h.get_text(" ", strip=True)
    if text:
        print(f"<{h.name} class={h.get('class')}> {text}")

print("\n--- divs with name/title/role/position/bio in class ---")
for div in soup2.find_all(True, class_=True):
    classes = " ".join(div.get("class", []))
    if any(k in classes.lower() for k in ["name","title","role","position","bio","card","member"]):
        t = div.get_text(" ", strip=True)[:150]
        if t:
            print(f"<{div.name} class='{classes}'> {t}")
