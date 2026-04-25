import sqlite3
from source.models import main_model

# Exporta BANCO_PATH para permitir monkeypatch nos testes
BANCO_PATH = main_model.BANCO_PATH


def save_new_url(url: str, code: str) -> None:
    conn = sqlite3.connect(BANCO_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO links (url, code) VALUES (?, ?)", (url, code,))

    conn.commit()
    conn.close()