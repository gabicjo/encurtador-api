import pytest
import random
import string
from unittest.mock import patch, MagicMock
from source.services.encurtar_service import generate_new_code, create_shortlink


class TestGenerateNewCode:
    @patch("source.services.encurtar_service.random")
    def test_generates_code_with_default_length(self, mock_random):
        mock_random.choice.side_effect = iter(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
        code = generate_new_code(10)
        assert len(code) == 10

    @patch("source.services.encurtar_service.random")
    def test_generates_code_with_custom_length(self, mock_random):
        mock_random.choice.side_effect = iter(["x", "y", "z"])
        code = generate_new_code(3)
        assert len(code) == 3

    @patch("source.services.encurtar_service.random")
    def test_generates_code_uses_ascii_letters_and_digits(self, mock_random):
        mock_random.choice.side_effect = iter(["A", "B", "1", "2"])
        code = generate_new_code(4)
        assert code.isalnum()


class TestCreateShortlink:
    @patch("source.services.encurtar_service.verify_code_exists")
    @patch("source.services.encurtar_service.encurtar_model")
    def test_creates_shortlink_with_unique_code(self, mock_model, mock_verify):
        mock_verify.return_value = None
        mock_save = MagicMock()
        mock_model.save_new_url = mock_save
        
        create_shortlink("https://example.com")
        
        mock_save.assert_called_once()
        call_args = mock_save.call_args[0]
        assert call_args[0] == "https://example.com"
        assert len(call_args[1]) == 10