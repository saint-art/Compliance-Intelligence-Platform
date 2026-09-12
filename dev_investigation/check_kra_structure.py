from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kra_leadership_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

lists = soup.find_all('ul', class_='leadership-list')
print(f'Found {len(lists)} leadership-list(s)')

for i, ul in enumerate(lists):
    items = ul.find_all('a', class_='cd-trigger')
    print(f'List {i+1}: {len(items)} people')
    prev = ul.find_previous(['h1', 'h2', 'h3', 'h4'])
    heading_text = prev.get_text(strip=True) if prev else "None"
    print(f'  Preceding heading: {heading_text!r}')
