import pytest
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash


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
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(256) NOT NULL
        )""")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def test_app(test_db_path, monkeypatch):
    import sys
    from pathlib import Path
    from werkzeug.security import generate_password_hash
    
    from flask import Flask
    from flask_cors import CORS
    from source.routes.encurtar_route import encurtar_bp
    from source.routes.redirect_route import redirect_bp
    from source.routes.auth_routes import auth_bp
    from source.models import main_model, users_model
    from source.auth import login_manager
    
    monkeypatch.chdir(Path(__file__).resolve().parent.parent.parent)
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret-key"
    CORS(app)
    
    login_manager.init_app(app)
    
    app.register_blueprint(encurtar_bp)
    app.register_blueprint(redirect_bp)
    app.register_blueprint(auth_bp)
    
    app.config["TESTING"] = True
    
    return app


@pytest.fixture
def client(test_app, test_db_path, monkeypatch):
    import source.models.main_model as main_model
    import source.models.encurtar_model as encurtar_model
    import source.models.users_model as users_model
    
    monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
    monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))
    monkeypatch.setattr(users_model, "BANCO_PATH", str(test_db_path))
    
    with test_app.test_client() as client:
        # Create test user and login
        conn = sqlite3.connect(str(test_db_path))
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("testuser", generate_password_hash("testpass"))
        )
        conn.commit()
        conn.close()
        
        # Login
        client.post("/login", json={"username": "testuser", "password": "testpass"})
        
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


class TestCustomCode:
    """Testes para códigos personalizados"""

    def test_creates_shortlink_with_custom_code(self, client, test_db_path, monkeypatch):
        """Deve criar link com código personalizado válido"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://example.com",
            "code": "custom"
        })
        assert response.status_code == 200

    def test_creates_shortlink_with_numeric_code(self, client, test_db_path, monkeypatch):
        """Deve criar link com código numérico"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://test.com",
            "code": "12345"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "12345" in data["url"]

    def test_returns_400_for_code_less_than_3_characters(self, client, test_db_path, monkeypatch):
        """Deve retornar 400 para código com menos de 3 caracteres"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://example.com",
            "code": "ab"
        })
        assert response.status_code == 400
        assert "3" in response.get_json()["message"]

    def test_returns_400_for_code_with_exactly_3_characters(self, client, test_db_path, monkeypatch):
        """Deve aceitar código com exatamente 3 caracteres"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://example.com",
            "code": "abc"
        })
        assert response.status_code == 200

    def test_returns_400_for_duplicate_custom_code(self, client, test_db_path, monkeypatch):
        """Deve retornar erro para código duplicado"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        import sqlite3
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        # Insere um link primeiro
        conn = sqlite3.connect(str(test_db_path))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)",
                      ("https://first.com", "existe", 0))
        conn.commit()
        conn.close()

        # Tenta criar outro com o mesmo código
        response = client.post("/encurtar", json={
            "url": "https://second.com",
            "code": "existe"
        })
        assert response.status_code == 400

    def test_custom_code_in_response_url(self, client, test_db_path, monkeypatch):
        """O código personalizado deve aparecer na URL de resposta"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://example.com",
            "code": "meulink"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "/meulink" in data["url"]

    def test_without_custom_code_uses_generated_code(self, client, test_db_path, monkeypatch):
        """Sem código personalizado, deve gerar automaticamente"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://example.com"
        })
        assert response.status_code == 200
        data = response.get_json()
        # Código gerado deve ter 10 caracteres
        code = data["url"].split("/")[-1]
        assert len(code) == 10

    def test_custom_code_with_mixed_characters(self, client, test_db_path, monkeypatch):
        """Deve aceitar código com caracteres mistos"""
        import source.models.main_model as main_model
        import source.models.encurtar_model as encurtar_model
        monkeypatch.setattr(main_model, "BANCO_PATH", str(test_db_path))
        monkeypatch.setattr(encurtar_model, "BANCO_PATH", str(test_db_path))

        response = client.post("/encurtar", json={
            "url": "https://mixed.com",
            "code": "Test123"
        })
        assert response.status_code == 200