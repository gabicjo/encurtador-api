import sqlite3
from source.models import main_model


def add_new_click(code):
    conn = sqlite3.connect(main_model.BANCO_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))

    conn.commit()
    conn.close()