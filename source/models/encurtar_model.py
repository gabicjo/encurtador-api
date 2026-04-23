import sqlite3

def verify_code_exists(code):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM links WHERE code = ?", (code,))
    return cursor.fetchone() 

def save_new_url(url, code):
    print(f"URL: {url}, CODE: {code}")
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO links (url, code) VALUES (?, ?)", (url, code,))

    conn.commit()
    conn.close()