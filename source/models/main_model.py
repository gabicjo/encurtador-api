import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

def criar_tabela():
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE
        )""")

def verify_code_exists(code):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM links WHERE code = ?", (code,))
    return cursor.fetchone() 
