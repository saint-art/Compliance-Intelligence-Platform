path = '.gitignore'
content = open(path).read()
old = """# ================================
# Generated / diagnostic artifacts
# ================================
*.html
*.csv"""
new = """# ================================
# Generated / diagnostic artifacts
# ================================
*.html
*.csv
!output/*.csv"""
if old not in content:
    print('ANCHOR_NOT_FOUND')
else:
    content = content.replace(old, new)
    open(path, 'w').write(content)
    print('PATCHED')
