import pytest
from unittest.mock import patch, MagicMock


class TestStatsService:
    """Testes para o stats_service"""

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_returns_data_for_existing_code(self, mock_verify):
        """Deve retornar estatísticas para código existente"""
        mock_verify.return_value = (1, "https://example.com", "abc123", 10)

        from source.services import stats_service
        result = stats_service.get_url_stats("abc123")

        assert result["url_original"] == "https://example.com"
        assert result["clicks"] == 10

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_raises_for_nonexistent_code(self, mock_verify):
        """Deve lançar exceção para código inexistente"""
        mock_verify.return_value = None

        from source.services import stats_service
        from source.error_handler import CodigoInvalido

        with pytest.raises(CodigoInvalido):
            stats_service.get_url_stats("nonexistent")

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_returns_correct_url(self, mock_verify):
        """Deve retornar URL original correta"""
        mock_verify.return_value = (2, "https://google.com", "goog", 0)

        from source.services import stats_service
        result = stats_service.get_url_stats("goog")

        assert result["url_original"] == "https://google.com"

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_returns_zero_clicks(self, mock_verify):
        """Deve retornar 0 cliques para link sem acessos"""
        mock_verify.return_value = (3, "https://new.com", "new", 0)

        from source.services import stats_service
        result = stats_service.get_url_stats("new")

        assert result["clicks"] == 0

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_returns_high_clicks(self, mock_verify):
        """Deve retornar contagem alta de cliques"""
        mock_verify.return_value = (4, "https://popular.com", "pop", 9999)

        from source.services import stats_service
        result = stats_service.get_url_stats("pop")

        assert result["clicks"] == 9999

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_calls_verify_with_code(self, mock_verify):
        """Deve chamar verify_code_exists com o código correto"""
        mock_verify.return_value = (1, "https://test.com", "test", 5)

        from source.services import stats_service
        stats_service.get_url_stats("test")

        mock_verify.assert_called_once_with("test")

    @patch("source.services.stats_service.verify_code_exists")
    def test_get_url_stats_handles_special_characters_in_url(self, mock_verify):
        """Deve lidar com URLs com caracteres especiais"""
        mock_verify.return_value = (1, "https://example.com/path?param=value&other=test", "special", 3)

        from source.services import stats_service
        result = stats_service.get_url_stats("special")

        assert "param=value" in result["url_original"]