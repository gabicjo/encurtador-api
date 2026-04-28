import pytest
import sqlite3
import os
from pathlib import Path


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_banco.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE,
        clicks INTEGER NOT NULL DEFAULT 0
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(256) NOT NULL
    )""")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def app(test_db, monkeypatch):
    from flask import Flask
    from flask_cors import CORS
    from source.routes.encurtar_route import encurtar_bp
    from source.routes.redirect_route import redirect_bp
    from source.routes.auth_routes import auth_bp
    from source.models import main_model, users_model
    from source.auth import login_manager
    
    monkeypatch.setenv("TEST_DB_PATH", str(test_db))
    monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(test_db))
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret-key"
    CORS(app)
    
    login_manager.init_app(app)
    
    app.register_blueprint(encurtar_bp)
    app.register_blueprint(redirect_bp)
    app.register_blueprint(auth_bp)
    
    return app


@pytest.fixture
def client(app):
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_client(client, test_db):
    """Client with authenticated user."""
    from werkzeug.security import generate_password_hash
    
    # Create test user
    conn = sqlite3.connect(str(test_db))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("testuser", generate_password_hash("testpass"))
    )
    conn.commit()
    conn.close()
    
    # Login
    client.post("/login", json={"username": "testuser", "password": "testpass"})
    
    return client