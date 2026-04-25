import random
import string
from source.models import encurtar_model
from source.models.main_model import verify_code_exists
from source import error_handler

def generate_new_code(tamanho: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(tamanho))
    return code


def create_shortlink(url: str) -> str:
    if verify_valid_url(url):
        while True:
            code = generate_new_code(10)
            if verify_code_exists(code) == None:
                break

        encurtar_model.save_new_url(url, code)
        return code
    else:
        raise error_handler.URLInvalido("URL sem protocolo http:// ou https://")

def create_custom_shortlink(url: str, code: str) -> str:
    if verify_valid_url(url):
        if verify_code_exists(code) == None:
            encurtar_model.save_new_url(url, code)
            return code
        raise error_handler.CodigoInvalido("O codigo enviado já existe")
    else:
        raise error_handler.URLInvalido("URL sem protocolo http:// ou https://")

def verify_valid_url(url: str) -> bool:
    valid_url_protocol = ['https://', "http://"]
    for protocol in valid_url_protocol:
        if url.startswith(protocol):
            return True
    return False