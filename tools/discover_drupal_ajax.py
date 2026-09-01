import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.parliament.go.ke"

URL = BASE + "/the-national-assembly/mps"

headers = {
    "User-Agent": "Compliance-Intelligence-Platform/1.0"
}

html = requests.get(URL, headers=headers).text

soup = BeautifulSoup(html, "html.parser")

keywords = [
    "views/ajax",
    "jsonapi",
    "drupalSettings",
    "ajax",
    "view_name",
    "view_display",
    "views",
    "load",
    "fetch",
]

print("=" * 80)
print("SCANNING JAVASCRIPT")
print("=" * 80)

for script in soup.find_all("script", src=True):

    src = urljoin(BASE, script["src"])

    print("\nDownloading:", src)

    try:

        js = requests.get(src, timeout=30).text

    except Exception:

        continue

    for word in keywords:

        if word in js:

            print("FOUND:", word)

            for m in re.finditer(word, js):

                start = max(0, m.start() - 150)

                end = min(len(js), m.end() + 300)

                print("-" * 40)
                print(js[start:end])