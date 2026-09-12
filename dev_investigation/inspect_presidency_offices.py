import requests
from bs4 import BeautifulSoup
from pathlib import Path

pages = {
    "office_of_the_president": "https://www.president.go.ke/administration/office-of-the-president/",
    "office_of_the_deputy_president": "https://www.president.go.ke/?page_id=493",
}

headers = {"User-Agent": "Compliance-Intelligence-Platform/1.0"}

Path("input/raw_html").mkdir(parents=True, exist_ok=True)

for name, url in pages.items():
    print(f"\n{'='*70}\nFETCHING: {name}\n{url}\n{'='*70}")

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text

    out_path = Path(f"input/raw_html/{name}_inspect.html")
    out_path.write_text(html, encoding="utf-8", errors="ignore")
    print(f"Saved -> {out_path}")

    soup = BeautifulSoup(html, "lxml")

    print("\n--- Headings (h1-h4) ---")
    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        text = tag.get_text(" ", strip=True)
        if text:
            print(f"<{tag.name} class={tag.get('class')}> {text}")

    print("\n--- Images with alt text mentioning name-like content ---")
    for img in soup.find_all("img"):
        alt = img.get("alt", "")
        src = img.get("data-src") or img.get("src", "")
        if alt:
            print(f"alt='{alt}' src={src} class={img.get('class')}")

    print("\n--- Divs with 'name' or 'title' or 'bio' in class ---")
    for div in soup.find_all("div", class_=True):
        classes = " ".join(div.get("class", []))
        if any(k in classes.lower() for k in ["name", "title", "bio", "profile", "position"]):
            text = div.get_text(" ", strip=True)[:150]
            print(f"class='{classes}' -> {text}")
