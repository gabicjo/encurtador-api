import pytest
import random
import string
from unittest.mock import patch, MagicMock
from source.services.encurtar_service import (
    generate_new_code,
    create_shortlink,
    create_custom_shortlink,
    verify_valid_url
)


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


class TestVerifyValidURL:
    """Testes para verify_valid_url"""

    def test_accepts_https_url(self):
        """Deve aceitar URLs com https"""
        assert verify_valid_url("https://example.com") is True

    def test_accepts_http_url(self):
        """Deve aceitar URLs com http"""
        assert verify_valid_url("http://example.com") is True

    def test_rejects_url_without_protocol(self):
        """Deve rejeitar URLs sem protocolo"""
        assert verify_valid_url("example.com") is False

    def test_rejects_ftp_protocol(self):
        """Deve rejeitar protocolo ftp"""
        assert verify_valid_url("ftp://example.com") is False

    def test_rejects_empty_url(self):
        """Deve rejeitar URL vazia"""
        assert verify_valid_url("") is False

    def test_rejects_other_protocols(self):
        """Deve rejeitar outros protocolos"""
        assert verify_valid_url("mailto:user@example.com") is False
        assert verify_valid_url("file:///path") is False


class TestCreateCustomShortlink:
    """Testes para create_custom_shortlink"""

    @patch("source.services.encurtar_service.verify_code_exists")
    @patch("source.services.encurtar_service.encurtar_model")
    def test_creates_custom_shortlink_with_valid_code(self, mock_model, mock_verify):
        """Deve criar link com código personalizado válido"""
        mock_verify.return_value = None
        mock_save = MagicMock()
        mock_model.save_new_url = mock_save

        create_custom_shortlink("https://example.com", "mycode")

        mock_save.assert_called_once_with("https://example.com", "mycode")

    @patch("source.services.encurtar_service.verify_code_exists")
    @patch("source.services.encurtar_service.encurtar_model")
    def test_raises_for_existing_code(self, mock_model, mock_verify):
        """Deve lançar exceção para código existente"""
        mock_verify.return_value = (1, "https://existing.com", "existing")

        from source.error_handler import CodigoInvalido
        with pytest.raises(CodigoInvalido):
            create_custom_shortlink("https://new.com", "existing")

    @patch("source.services.encurtar_service.verify_code_exists")
    @patch("source.services.encurtar_service.encurtar_model")
    def test_raises_for_invalid_url(self, mock_model, mock_verify):
        """Deve lançar exceção para URL inválida"""
        mock_verify.return_value = None

        from source.error_handler import URLInvalido
        with pytest.raises(URLInvalido):
            create_custom_shortlink("invalid-url", "mycode")

    @patch("source.services.encurtar_service.verify_code_exists")
    @patch("source.services.encurtar_service.encurtar_model")
    def test_returns_code_on_success(self, mock_model, mock_verify):
        """Deve retornar o código em caso de sucesso"""
        mock_verify.return_value = None
        mock_save = MagicMock()
        mock_model.save_new_url = mock_save

        result = create_custom_shortlink("https://example.com", "custom")

        assert result == "custom"