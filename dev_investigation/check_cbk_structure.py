from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/cbk_governance_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

el = soup.find(string=lambda s: s and 'Musangi' in s)
if el:
    print("Found Musangi in:", el.parent.name, el.parent.get('class'))
    parent = el.parent
    for level in range(6):
        parent = parent.parent
        if parent is None:
            break
        print(f"--- Level {level+1}: <{parent.name} class={parent.get('class')}> ---")
        print(parent.get_text(' ', strip=True)[:150])
        print()
else:
    print("Musangi not found in page text")
    print(soup.get_text(' ', strip=True)[:500])
