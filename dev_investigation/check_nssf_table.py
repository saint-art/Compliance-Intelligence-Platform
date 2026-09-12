from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/nssf_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

container = soup.find('div', class_='board_members')
print(container.prettify()[:3000])
