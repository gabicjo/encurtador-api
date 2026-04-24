import sqlite3

def save_new_url(url, code):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO links (url, code) VALUES (?, ?)", (url, code,))

    conn.commit()
    conn.close()