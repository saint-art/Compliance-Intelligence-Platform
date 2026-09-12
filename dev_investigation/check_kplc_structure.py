from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kplc_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

# Look for a heading naming a known board member
target = None
for tag in soup.find_all(['h1','h2','h3','h4','h5','h6']):
    text = tag.get_text(' ', strip=True)
    if 'Masinde' in text or 'Bwauma' in text:
        target = tag
        break

if target:
    print(f"Found: <{target.name}> {target.get_text(strip=True)}")
    parent = target
    for level in range(5):
        parent = parent.parent
        if parent is None:
            break
        print(f"--- Level {level+1}: <{parent.name} class={parent.get('class')}> ---")
        text = parent.get_text(' ', strip=True)
        print(text[:200])
        print()
else:
    print("Not found in headings, trying all tags with that text")
    el = soup.find(string=lambda s: s and 'Masinde' in s)
    if el:
        print("Found in:", el.parent.name, el.parent.get('class'))
        print(el.parent.prettify()[:1000])
    else:
        print("Masinde not found anywhere in page text")
