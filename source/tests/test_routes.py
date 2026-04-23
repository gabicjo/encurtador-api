import pytest
import sqlite3
from pathlib import Path


@pytest.fixture
def test_db_path(tmp_path):
    db_path = tmp_path / "test_banco.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE
    )""")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def test_app(test_db_path, monkeypatch):
    import sys
    from pathlib import Path
    
    from flask import Flask
    from flask_cors import CORS
    from source.routes.encurtar_route import encurtar_bp
    from source.routes.redirect_route import redirect_bp
    
    monkeypatch.chdir(Path(__file__).resolve().parent.parent.parent)
    
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(encurtar_bp)
    app.register_blueprint(redirect_bp)
    
    app.config["TESTING"] = True
    
    return app


@pytest.fixture
def client(test_app, test_db_path, monkeypatch):
    monkeypatch.setattr("source.models.encurtar_model.sqlite3", __import__("sqlite3"))
    
    with test_app.test_client() as client:
        yield client


class TestEncurtarRoute:
    def test_returns_400_when_no_url_provided(self, client):
        response = client.post("/encurtar", json={})
        assert response.status_code == 400
        assert "URL" in response.get_json()["message"]

    def test_returns_400_for_empty_url(self, client):
        response = client.post("/encurtar", json={"url": ""})
        assert response.status_code == 400

    def test_returns_400_for_none_url(self, client):
        response = client.post("/encurtar", json={"url": None})
        assert response.status_code == 400

    def test_returns_400_for_url_without_protocol(self, client):
        response = client.post("/encurtar", json={"url": "example.com"})
        assert response.status_code == 400
        assert "http" in response.get_json()["message"]

    def test_returns_400_for_url_with_invalid_protocol(self, client):
        response = client.post("/encurtar", json={"url": "ftp://example.com"})
        assert response.status_code == 400


class TestRedirectRoute:
    def test_returns_404_for_nonexistent_code(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404