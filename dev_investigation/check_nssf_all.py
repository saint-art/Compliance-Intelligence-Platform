from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/nssf_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

container = soup.find('div', class_='board_members')
paragraphs = container.find_all('p')
print(f"Found {len(paragraphs)} paragraph(s)\n")
for p in paragraphs:
    text = p.get_text(' ', strip=True)
    if text:
        print(repr(text))
