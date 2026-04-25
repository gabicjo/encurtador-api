import sqlite3

BANCO_PATH = "banco.db"


def criar_tabela() -> None:
    with sqlite3.connect(BANCO_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR(200) NOT NULL,
            code VARCHAR(30) NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
            )""")


def verify_code_exists(code: str) -> tuple:
    with sqlite3.connect(BANCO_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM links WHERE code = ?", (code,))

        return cursor.fetchone()

criar_tabela()