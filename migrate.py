import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace imports
content = content.replace('import mysql.connector', 'import sqlite3')

# 2. Replace connection function
# Using a precise string replacement since the function is known.
old_conn_func = """def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )"""

new_conn_func = """def get_db_connection():
    import config
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn"""

if old_conn_func in content:
    content = content.replace(old_conn_func, new_conn_func)
else:
    print("Could not find old get_db_connection function. Trying regex...")
    content = re.sub(
        r'def get_db_connection\(\):\s+return mysql\.connector\.connect\([\s\S]*?\n    \)',
        new_conn_func,
        content
    )

# 3. Replace cursor(dictionary=True) with cursor()
content = content.replace('cursor(dictionary=True)', 'cursor()')

# 4. Replace AUTO_INCREMENT with AUTOINCREMENT
content = content.replace('AUTO_INCREMENT', 'AUTOINCREMENT')

# 5. Replace MySQL exceptions
content = content.replace('mysql.connector.Error', 'sqlite3.Error')

# 6. Replace %s with ? ONLY in cursor.execute or query strings
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'logger' not in line and not line.strip().startswith('#'):
        new_lines.append(line.replace('%s', '?'))
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Migration script completed.")
