import pytest
from source.error_handler import URLInvalido, SemURL


class TestURLInvalido:
    def test_can_instantiate_with_message(self):
        msg = "URL inválido"
        exc = URLInvalido(msg)
        assert str(exc) == msg

    def test_can_instantiate_without_message(self):
        exc = URLInvalido()
        assert str(exc) == ""

    def test_is_exception(self):
        exc = URLInvalido("test")
        assert isinstance(exc, Exception)


class TestSemURL:
    def test_can_instantiate_with_message(self):
        msg = "URL não enviado"
        exc = SemURL(msg)
        assert str(exc) == msg

    def test_can_instantiate_without_message(self):
        exc = SemURL()
        assert str(exc) == ""

    def test_is_exception(self):
        exc = SemURL("test")
        assert isinstance(exc, Exception)