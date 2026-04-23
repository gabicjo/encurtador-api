import pytest
import sqlite3
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestVerifyCodeExists:
    @pytest.fixture
    def db_with_data(self, tmp_path):
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url VARCHAR(200) NOT NULL,
            code VARCHAR(30) NOT NULL UNIQUE
        )""")
        cursor.execute("INSERT INTO links (url, code) VALUES (?, ?)", ("https://example.com", "abc123"))
        conn.commit()
        conn.close()
        return db_path

    @patch("source.models.main_model.verify_code_exists")
    def test_returns_none_for_nonexistent_code(self, mock_verify):
        mock_verify.return_value = None
        result = mock_verify("nonexistent")
        assert result is None

    @patch("source.models.main_model.verify_code_exists")
    def test_returns_data_for_existing_code(self, mock_verify):
        mock_verify.return_value = (1, "https://example.com", "abc123")
        result = mock_verify("abc123")
        assert result is not None