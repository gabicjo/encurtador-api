import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Exporta BANCO_PATH para permitir monkeypatch nos testes
from source.models import main_model
BANCO_PATH = main_model.BANCO_PATH


def criar_tabela_users() -> None:
    with sqlite3.connect(BANCO_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(256) NOT NULL
        )""")


class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def create(username: str, password: str) -> "User":
        hash_ = generate_password_hash(password)
        with sqlite3.connect(BANCO_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_)
            )
            cursor.execute("SELECT last_insert_rowid()")
            user_id = cursor.fetchone()[0]
        return User(user_id, username, hash_)

    @staticmethod
    def get_by_username(username: str) -> "User | None":
        with sqlite3.connect(BANCO_PATH) as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            if row:
                return User(row[0], row[1], row[2])
            return None

    @staticmethod
    def get_by_id(user_id: int) -> "User | None":
        with sqlite3.connect(BANCO_PATH) as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row:
                return User(row[0], row[1], row[2])
            return None

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)