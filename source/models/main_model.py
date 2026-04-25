import sqlite3

BANCO_PATH = "banco.db"


def criar_tabela() -> None:
    conn = sqlite3.connect(BANCO_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE,
        clicks INTEGER NOT NULL DEFAULT 0
        )""")

    conn.commit()
    conn.close()


def verify_code_exists(code: str) -> tuple:
    conn = sqlite3.connect(BANCO_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM links WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result 

criar_tabela()