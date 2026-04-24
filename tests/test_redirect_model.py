import pytest
import sqlite3
from pathlib import Path


class TestAddNewClick:
    @pytest.fixture
    def db_with_link(self, tmp_path):
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR(200) NOT NULL,
            code VARCHAR(30) NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
        )""")
        cursor.execute("INSERT INTO links (url, code, clicks) VALUES (?, ?, ?)", ("https://example.com", "abc123", 0))
        conn.commit()
        conn.close()
        return db_path

    def test_increments_click_count(self, db_with_link, monkeypatch):
        from source.models import redirect_model
        monkeypatch.setattr(redirect_model, "BANCO_PATH", str(db_with_link))

        redirect_model.add_new_click("abc123")

        conn = sqlite3.connect(str(db_with_link))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("abc123",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 1

    def test_increments_multiple_times(self, db_with_link, monkeypatch):
        from source.models import redirect_model
        monkeypatch.setattr(redirect_model, "BANCO_PATH", str(db_with_link))

        redirect_model.add_new_click("abc123")
        redirect_model.add_new_click("abc123")
        redirect_model.add_new_click("abc123")

        conn = sqlite3.connect(str(db_with_link))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("abc123",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 3

    def test_no_change_for_nonexistent_code(self, db_with_link, monkeypatch):
        from source.models import redirect_model
        monkeypatch.setattr(redirect_model, "BANCO_PATH", str(db_with_link))

        redirect_model.add_new_click("nonexistent")

        conn = sqlite3.connect(str(db_with_link))
        cursor = conn.cursor()
        cursor.execute("SELECT clicks FROM links WHERE code = ?", ("abc123",))
        result = cursor.fetchone()
        conn.close()

        assert result[0] == 0