from source.models.main_model import verify_code_exists
from source import error_handler

def get_url_stats(code):
    url_data = verify_code_exists(code)
    if url_data:
        return {
            "url_original": url_data[1],
            "clicks": url_data[3]
        }
    raise error_handler.CodigoInvalido("O codigo enviado não existe.")