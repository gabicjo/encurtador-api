from flask import Blueprint, request, jsonify
from source.services.encurtar_service import create_shortlink
from source import error_handler
import sys

encurtar_bp = Blueprint("encurtar", __name__)


def _get_base_url():
    host = request.host
    if request.host[0] == '[':
        host_without_port = host.split(']:')[0] + ']'
    elif ':' in host:
        host_without_port = host.split(':')[0]
    else:
        host_without_port = host
    return f"{request.scheme}://{host_without_port}"


@encurtar_bp.route("/encurtar", methods=["POST"])
def generate_code():
    data = request.json

    try:
        if "url" in data:
            if data['url'] not in [None, ""]:
                code = create_shortlink(data['url'])
                base_url = _get_base_url()
                return jsonify({"url": f"{base_url}/{code}"})

            raise error_handler.URLInvalido("O URL recebido é invalido")

        raise error_handler.SemURL("URL não foi enviado")

    except error_handler.SemURL as e:
        return jsonify({"message": str(e)}), 400

    except error_handler.URLInvalido as e:
        return jsonify({"message": str(e)}), 400
