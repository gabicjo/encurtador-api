import sqlite3

BANCO_PATH = "banco.db"


def criar_tabela():
    conn = sqlite3.connect(BANCO_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE
        )""")
    conn.commit()
    conn.close()


def verify_code_exists(code):
    conn = sqlite3.connect(BANCO_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM links WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result 
