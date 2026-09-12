from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kplc_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

divs = soup.select('div.text-lg.font-bold.text-white')
print(f"Found {len(divs)} name/title divs\n")
for d in divs:
    print(repr(d.get_text(' ', strip=True)))
