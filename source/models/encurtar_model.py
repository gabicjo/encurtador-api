import sqlite3
from source.models import main_model


def save_new_url(url: str, code: str) -> None:
    conn = sqlite3.connect(main_model.BANCO_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO links (url, code) VALUES (?, ?)", (url, code,))

    conn.commit()
    conn.close()