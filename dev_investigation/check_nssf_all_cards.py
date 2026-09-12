from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/nssf_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

cards = soup.find_all('div', class_='board_members')
print(f"Found {len(cards)} card(s)\n")

for card in cards:
    p = card.find('p')
    img = card.find('img')
    text = p.get_text(' ', strip=True) if p else None
    src = img.get('src') if img else None
    print(f"{text!r}  img={src}")
