from flask import Blueprint, abort, redirect

from source.models.main_model import verify_code_exists
from source.services import redirect_service

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.route("/<code>", methods=["GET"])
def redirect_to_link(code: str):
    """
    Redireciona para a URL original.
    
    Encontra a URL original correspondente ao código curto
    e redireciona para ela. Incrementa o contador de cliques.
    ---
    tags:
      - Redirecionar
    summary: Redirecionar para URL original
    description: Redireciona para a URL original usando o código curto
    produces:
      - text/html
    parameters:
      - in: path
        name: code
        type: string
        required: true
        description: Código curto da URL
        example: abc123
    responses:
      302:
        description: Redirecionamento temporário para a URL original
      404:
        description: Código não encontrado
        schema:
          type: object
          properties:
            message:
              type: string
    """
    url_data = verify_code_exists(code)
    if url_data:
        redirect_service.add_new_click(code)
        return redirect(url_data[1])
    return abort(404)