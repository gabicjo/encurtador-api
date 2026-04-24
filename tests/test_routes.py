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
            code VARCHAR(30) NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
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
    import source.models.main_model as main_model
    monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
    
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

    def test_redirect_increments_click_count(self, client, test_db_path, monkeypatch):
        import source.models.main_model as main_model
        import source.models.redirect_model as redirect_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(redirect_model, "BANCO_PATH", str(test_db_path))

        import sqlite3
        conn = sqlite3.connect(str(test_db_path))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", ("https://example.com", "test123", 0))
        conn.commit()
        conn.close()

        client.get("/test123")

        conn = sqlite3.connect(str(test_db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("test123",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 1

    def test_multiple_redirects_increment_clicks(self, client, test_db_path, monkeypatch):
        import source.models.main_model as main_model
        import source.models.redirect_model as redirect_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(redirect_model, "BANCO_PATH", str(test_db_path))

        import sqlite3
        conn = sqlite3.connect(str(test_db_path))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", ("https://example.com", "test456", 0))
        conn.commit()
        conn.close()

        client.get("/test456")
        client.get("/test456")
        client.get("/test456")

        conn = sqlite3.connect(str(test_db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("test456",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 3