from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kpc_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

body_text = soup.get_text(' ', strip=True)
print(f"Body text length: {len(body_text)}")
print(f"First 300 chars: {body_text[:300]}")
print()

# Try to find a name-like heading
for tag in soup.find_all(['h1','h2','h3','h4','h5','h6']):
    text = tag.get_text(' ', strip=True)
    if text and len(text) < 60 and any(c.isupper() for c in text):
        print(f"<{tag.name} class={tag.get('class')}> {text}")
