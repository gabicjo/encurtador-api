from flask import Blueprint, jsonify, request
from source.services import encurtar_service
from source import error_handler

encurtar_bp = Blueprint("encurtar", __name__)


def _get_base_url() -> str:
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
    """
    Cria uma URL encurtada.
    
    Cria uma nova URL encurtada ou usa um código personalizado
    se fornecido (mínimo 3 caracteres).
    ---
    tags:
      - Encurtar URL
    summary: Criar URL encurtada
    description: Cria uma nova URL encurtada. Opcionalmente fornece um código personalizado com no mínimo 3 caracteres.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - url
          properties:
            url:
              type: string
              format: url
              example: https://www.google.com
              description: URL original a ser encurtada
            code:
              type: string
              minLength: 3
              maxLength: 30
              example: google
              description: Código personalizado opcional (mínimo 3 caracteres)
    responses:
      200:
        description: URL encurtada criada com sucesso
        schema:
          type: object
          properties:
            url:
              type: string
              example: http://localhost:9284/abc123xyz
        examples:
          application/json:
            url: "http://localhost:9284/abc123xyz"
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: "URL não foi enviado"
          application/json:
            message: "O URL recebido é invalido"
          application/json:
            message: "O codigo precisa ter pelo menos 3 caracteres"
    """
    data = request.json

    try:
        if "url" in data:
            if data['url'] not in [None, ""]:
                if "code" in data:
                    if len(data['code']) >= 3:
                        code = encurtar_service.create_custom_shortlink(data['url'], data['code'])
                    else:
                        raise error_handler.CodigoInvalido("O codigo precisa ter pelo menos 3 caracteres")

                else:
                    code = encurtar_service.create_shortlink(data['url'])

                base_url = _get_base_url()

                return jsonify({"url": f"{base_url}/{code}"})
            raise error_handler.URLInvalido("O URL recebido é invalido")
        raise error_handler.SemURL("URL não foi enviado")

    except error_handler.SemURL as e:
        return jsonify({"message": str(e)}), 400

    except error_handler.URLInvalido as e:
        return jsonify({"message": str(e)}), 400
    
    except error_handler.CodigoInvalido as e:
        return jsonify({"message": str(e)}), 400