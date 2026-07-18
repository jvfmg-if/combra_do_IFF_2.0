import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'instance', 'flaskr.sqlite')
schema_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'schema.sql')

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
with open(schema_path) as f:
    conn.executescript(f.read())
conn.close()
print('Banco de dados inicializado.')
