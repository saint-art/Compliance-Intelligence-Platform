import re
import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.parliament.go.ke/the-national-assembly/mps"

headers = {
    "User-Agent": "Compliance-Intelligence-Platform/1.0"
}

print("=" * 80)
print("DOWNLOADING PAGE")
print("=" * 80)

html = requests.get(URL, headers=headers, timeout=30).text

print(f"Downloaded {len(html):,} characters")

soup = BeautifulSoup(html, "html.parser")

print()
print("=" * 80)
print("SCRIPT FILES")
print("=" * 80)

for script in soup.find_all("script", src=True):
    print(script["src"])

print()
print("=" * 80)
print("INLINE JSON")
print("=" * 80)

for script in soup.find_all("script"):

    t = script.get("type", "")

    if "json" in t.lower():

        print("-" * 40)
        print(t)
        print(script.text[:500])

print()
print("=" * 80)
print("POSSIBLE API ENDPOINTS")
print("=" * 80)

patterns = [
    r"/views/ajax[^\"']*",
    r"/jsonapi[^\"']*",
    r"/api[^\"']*",
    r"/rest[^\"']*",
    r"/node/\d+",
    r"/user/\d+",
]

found = set()

for pattern in patterns:
    for match in re.findall(pattern, html):
        found.add(match)

for endpoint in sorted(found):
    print(endpoint)

print()
print("=" * 80)
print("PROFILE LINKS")
print("=" * 80)

for a in soup.find_all("a", href=True):

    href = a["href"]

    if href.startswith("/hon-"):
        print(href)

print()
print("=" * 80)
print("DRUPAL SETTINGS")
print("=" * 80)

match = re.search(r"drupalSettings\s*=\s*(\{.*?\});", html, re.S)

if match:

    print("Found drupalSettings")
    print(match.group(1)[:1500])

else:

    print("No drupalSettings found")

print()
print("=" * 80)
print("DONE")
print("=" * 80)