from flask import Blueprint, request, jsonify
from source.services.encurtar_service import create_shortlink
from source import error_handler

encurtar_bp = Blueprint("encurtar", __name__)

@encurtar_bp.route("/encurtar", methods=["POST"])
def generate_code():
    data = request.json

    try:
        if "url" in data:
            if data['url'] not in [None, ""]:
                create_shortlink(data['url'])
                return jsonify({"message": "ok"})

            raise error_handler.URLInvalido("O URL recebido é invalido")

        raise error_handler.SemURL("URL não foi enviado")

    except error_handler.SemURL:
        return jsonify({"message": "URL não foi enviado"}), 400

    except error_handler.URLInvalido:
        return jsonify({"message": "O URL recebido é invalido"}), 400