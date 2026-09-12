from bs4 import BeautifulSoup
from pathlib import Path

html = Path('input/raw_html/kengen_team_inspect.html').read_text(encoding='utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

body_text = soup.get_text(' ', strip=True)
print(f"Body text length: {len(body_text)}")
print(f"First 500 chars: {body_text[:500]}")
print()
print("Script tags found:", len(soup.find_all('script')))
print("Contains 'react' or 'vue' or 'next':", any(k in html.lower() for k in ['react', 'vue', '__next', 'nuxt']))
