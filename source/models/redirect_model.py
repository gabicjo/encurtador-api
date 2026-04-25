import sqlite3
from source.models import main_model

# Exporta BANCO_PATH para permitir monkeypatch nos testes
BANCO_PATH = main_model.BANCO_PATH


def add_new_click(code: str) -> None:
    with sqlite3.connect(BANCO_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))