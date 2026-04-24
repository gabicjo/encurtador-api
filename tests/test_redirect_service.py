import pytest
from unittest.mock import patch, MagicMock


class TestRedirectService:
    @patch("source.models.redirect_model.add_new_click")
    def test_delegates_to_model(self, mock_add_click):
        from source.services import redirect_service

        redirect_service.add_new_click("abc123")

        mock_add_click.assert_called_once_with("abc123")

    @patch("source.models.redirect_model.add_new_click")
    def test_passes_correct_code(self, mock_add_click):
        from source.services import redirect_service

        redirect_service.add_new_click("xyz789")

        mock_add_click.assert_called_once_with("xyz789")