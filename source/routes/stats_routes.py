from flask import Blueprint, jsonify

from source import error_handler
from source.services import stats_service

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats/<code>", methods=["GET"])
def get_url_stats(code: str):
    """
    Retorna estatísticas de uma URL encurtada.
    
    Fornece a URL original e o número de cliques (visitas)
    para uma URL encurtada específica.
    ---
    tags:
      - Estatísticas
    summary: Obter estatísticas de URL
    description: Retorna a URL original e contagem de cliques para o código fornecido
    produces:
      - application/json
    parameters:
      - in: path
        name: code
        type: string
        required: true
        description: Código curto da URL
        example: abc123
    responses:
      200:
        description: Estatísticas retornadas com sucesso
        schema:
          type: object
          properties:
            url_original:
              type: string
              example: "https://www.google.com"
            clicks:
              type: integer
              example: 42
      404:
        description: Código não encontrado
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        stats = stats_service.get_url_stats(code)
        return jsonify(stats)
        
    except error_handler.CodigoInvalido as e:
        return jsonify({"message": str(e)}), 404