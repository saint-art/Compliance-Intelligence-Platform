path = "app.py"
content = open(path).read()

old = '''if __name__ == "__main__":
    app.run(debug=True, port=5000)'''

new = '''if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)'''

if old not in content:
    print("ANCHOR_NOT_FOUND")
else:
    content = content.replace(old, new)
    open(path, "w").write(content)
    print("PATCHED")
