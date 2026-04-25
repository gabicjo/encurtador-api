import pytest
import sqlite3
from pathlib import Path


class TestEncurtarModel:
    """Testes para o encurtar_model (salvar URLs no banco)"""

    @pytest.fixture
    def empty_db(self, tmp_path):
        """Cria banco de teste vazio"""
        db_path = tmp_path / "test.db"
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
    def app_with_db(self, empty_db, monkeypatch):
        from source.models import encurtar_model
        monkeypatch.setattr(encurtar_model, "sqlite3", sqlite3)
        return empty_db

    def test_save_new_url_inserts_into_database(self, empty_db, monkeypatch):
        """Deve inserir URL no banco de dados"""
        from source.models import encurtar_model

        # Patch do sqlite3.connect para usar nosso banco de teste
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(empty_db))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        encurtar_model.save_new_url("https://example.com", "abc123")

        # Verifica que foi inserido
        conn = sqlite3.connect(str(empty_db))
        cursor = conn.cursor()
        cursor.execute("SELECT url, code FROM links WHERE code = ?", ("abc123",))
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[0] == "https://example.com"
        assert result[1] == "abc123"

    def test_save_new_url_with_custom_code(self, empty_db, monkeypatch):
        """Deve salvar URL com código personalizado"""
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(empty_db))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        from source.models import encurtar_model
        encurtar_model.save_new_url("https://custom.com", "mycode")

        conn = sqlite3.connect(str(empty_db))
        cursor = conn.cursor()
        cursor.execute("SELECT url, code FROM links WHERE code = ?", ("mycode",))
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[0] == "https://custom.com"

    def test_save_new_url_sets_default_clicks_to_zero(self, empty_db, monkeypatch):
        """Deve definir clicks como 0 por padrão"""
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(empty_db))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        from source.models import encurtar_model
        encurtar_model.save_new_url("https://test.com", "test123")

        conn = sqlite3.connect(str(empty_db))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("test123",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 0

    def test_save_new_url_fails_with_duplicate_code(self, empty_db, monkeypatch):
        """Deve falhar se o código já existe"""
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(empty_db))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        from source.models import encurtar_model
        encurtar_model.save_new_url("https://first.com", "dupcode")

        # Tenta inserir novamente com o mesmo código
        with pytest.raises(sqlite3.IntegrityError):
            encurtar_model.save_new_url("https://second.com", "dupcode")

    def test_save_new_url_handles_long_url(self, empty_db, monkeypatch):
        """Deve lidar com URLs longas"""
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(empty_db))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        long_url = "https://example.com/" + "a" * 200
        from source.models import encurtar_model
        encurtar_model.save_new_url(long_url, "longurl")

        conn = sqlite3.connect(str(empty_db))
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM links WHERE code = ?", ("longurl",))
        result = cursor.fetchone()
        conn.close()

        assert result is not None


class TestEncurtarModelIntegration:
    """Testes de integração para encurtar_model com banco real"""

    @pytest.fixture
    def db_with_links(self, tmp_path):
        """Cria banco com alguns links"""
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR(200) NOT NULL,
            code VARCHAR(30) NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
        )""")
        # Insere alguns links
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)",
                    ("https://google.com", "google", 10))
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)",
                    ("https://github.com", "github", 5))
        conn.commit()
        conn.close()
        return db_path

    def test_multiple_urls_can_be_saved(self, db_with_links, monkeypatch):
        """Múltiplas URLs podem ser salvas"""
        original_connect = sqlite3.connect

        def mock_connect(path):
            return original_connect(str(db_with_links))

        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        from source.models import encurtar_model
        encurtar_model.save_new_url("https://new1.com", "new1")
        encurtar_model.save_new_url("https://new2.com", "new2")

        conn = sqlite3.connect(str(db_with_links))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM links")
        count = cursor.fetchone()[0]
        conn.close()

        # Deveria ter 4 links (2 existentes + 2 novos)
        assert count == 4