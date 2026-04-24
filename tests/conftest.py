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
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def app(test_db, monkeypatch):
    from flask import Flask
    from flask_cors import CORS
    from source.routes.encurtar_route import encurtar_bp
    from source.routes.redirect_route import redirect_bp
    
    monkeypatch.setenv("TEST_DB_PATH", str(test_db))
    
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(encurtar_bp)
    app.register_blueprint(redirect_bp)
    
    return app


@pytest.fixture
def client(app):
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client