from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kpc_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

scripts = soup.find_all('script')
print(f"Found {len(scripts)} script tags")

for s in scripts:
    text = s.get_text()
    if 'chairman' in text.lower() or 'director' in text.lower() or 'board' in text.lower():
        print("--- POSSIBLE MATCH ---")
        print(text[:500])
        print()

# Also check for any elementor widget referencing a slider/carousel with data
for div in soup.find_all('div', attrs={'data-widget_type': True}):
    print(div.get('data-widget_type'))
