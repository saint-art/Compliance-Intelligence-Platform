path = ".gitignore"
content = open(path).read()
old = """# ================================
# Local databases
# ================================
*.db
*.sqlite
*.sqlite3"""
new = """# ================================
# Local databases
# ================================
*.db
*.sqlite
*.sqlite3
!database/compliance.db"""
if old not in content:
    print("ANCHOR_NOT_FOUND")
else:
    content = content.replace(old, new)
    open(path, "w").write(content)
    print("PATCHED")
