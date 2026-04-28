import pytest
from source.services.auth_service import register, authenticate
from source.models.users_model import User
from source import error_handler


def test_register_success(tmp_path, monkeypatch):
    """Test successful user registration."""
    from source.models import users_model, main_model
    
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(main_model, "BANCO_PATH", str(db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(db_path))
    
    # Create tables
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.commit()
    conn.close()
    
    user = register("testuser", "password123")
    
    assert user.username == "testuser"
    assert user.id is not None


def test_register_duplicate_username(tmp_path, monkeypatch):
    """Test registration with duplicate username fails."""
    from source.models import users_model, main_model
    
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(main_model, "BANCO_PATH", str(db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(db_path))
    
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("existing", "hash")
    )
    conn.commit()
    conn.close()
    
    with pytest.raises(error_handler.CodigoInvalido):
        register("existing", "password123")


def test_authenticate_success(tmp_path, monkeypatch):
    """Test successful authentication."""
    from source.models import users_model, main_model
    from werkzeug.security import generate_password_hash
    
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(main_model, "BANCO_PATH", str(db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(db_path))
    
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("testuser", generate_password_hash("password123"))
    )
    conn.commit()
    conn.close()
    
    user = authenticate("testuser", "password123")
    
    assert user is not None
    assert user.username == "testuser"


def test_authenticate_wrong_password(tmp_path, monkeypatch):
    """Test authentication with wrong password returns None."""
    from source.models import users_model, main_model
    from werkzeug.security import generate_password_hash
    
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(main_model, "BANCO_PATH", str(db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(db_path))
    
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("testuser", generate_password_hash("password123"))
    )
    conn.commit()
    conn.close()
    
    user = authenticate("testuser", "wrongpassword")
    
    assert user is None


def test_authenticate_nonexistent_user(tmp_path, monkeypatch):
    """Test authentication with nonexistent user returns None."""
    from source.models import users_model, main_model
    
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(main_model, "BANCO_PATH", str(db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(db_path))
    
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.commit()
    conn.close()
    
    user = authenticate("nonexistent", "password123")
    
    assert user is None