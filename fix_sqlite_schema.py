import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace INT AUTOINCREMENT PRIMARY KEY -> INTEGER PRIMARY KEY AUTOINCREMENT
content = re.sub(r'INT\s+AUTOINCREMENT\s+PRIMARY\s+KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', content, flags=re.IGNORECASE)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
