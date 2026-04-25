import pytest
import sqlite3
from pathlib import Path


@pytest.fixture
def test_db_with_link(tmp_path):
    """Cria banco de teste com um link existente"""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(200) NOT NULL,
        code VARCHAR(30) NOT NULL UNIQUE,
        clicks INTEGER NOT NULL DEFAULT 0
    )""")
    cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", (
        "https://example.com", "testcode", 5
    ))
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def test_app(test_db_with_link, monkeypatch):
    from flask import Flask
    from flask_cors import CORS
    from source.routes.stats_routes import stats_bp
    from source.routes.redirect_route import redirect_bp

    monkeypatch.setattr("source.models.main_model.BANCO_PATH", str(test_db_with_link))
    monkeypatch.setattr("source.models.redirect_model.BANCO_PATH", str(test_db_with_link))

    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(stats_bp)
    app.register_blueprint(redirect_bp)
    app.config["TESTING"] = True

    return app


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client


class TestStatsRoute:
    """Testes para a rota /stats/<code>"""

    def test_returns_stats_for_existing_code(self, client):
        """Deve retornar estatísticas para código existente"""
        response = client.get("/stats/testcode")
        assert response.status_code == 200

        data = response.get_json()
        assert "url_original" in data
        assert "clicks" in data
        assert data["url_original"] == "https://example.com"
        assert data["clicks"] == 5

    def test_returns_404_for_nonexistent_code(self, client):
        """Deve retornar 404 para código inexistente"""
        response = client.get("/stats/nonexistent")
        assert response.status_code == 404

    def test_returns_404_with_message_for_nonexistent_code(self, client):
        """Deve retornar mensagem de erro para código inexistente"""
        response = client.get("/stats/naoexiste")
        data = response.get_json()
        assert "message" in data
        assert "codigo" in data["message"].lower()

    def test_stats_with_zero_clicks(self, client, test_db_with_link, monkeypatch):
        """Deve retornar 0 clicks para link sem acessos"""
        monkeypatch.setattr("source.models.main_model.BANCO_PATH", str(test_db_with_link))

        conn = sqlite3.connect(str(test_db_with_link))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", (
            "https://new.com", "zeroclicks", 0
        ))
        conn.commit()
        conn.close()

        response = client.get("/stats/zeroclicks")
        assert response.status_code == 200
        assert response.get_json()["clicks"] == 0

    def test_stats_with_many_clicks(self, client, test_db_with_link, monkeypatch):
        """Deve retornar contagem correta para muitos cliques"""
        monkeypatch.setattr("source.models.main_model.BANCO_PATH", str(test_db_with_link))

        conn = sqlite3.connect(str(test_db_with_link))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", (
            "https://popular.com", "popular", 1000
        ))
        conn.commit()
        conn.close()

        response = client.get("/stats/popular")
        assert response.status_code == 200
        assert response.get_json()["clicks"] == 1000