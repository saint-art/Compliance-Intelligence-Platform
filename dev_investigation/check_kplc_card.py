from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kplc_board_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

target = soup.find(string=lambda s: s and 'Masinde' in s)
name_div = target.parent

parent = name_div
for level in range(6):
    parent = parent.parent
    if parent is None:
        break
    classes = parent.get('class')
    text = parent.get_text(' ', strip=True)[:150]
    print(f"--- Level {level+1}: <{parent.name} class={classes}> ---")
    print(text)
    img = parent.find('img')
    if img:
        print(f"  IMG src: {img.get('src')}")
    print()
