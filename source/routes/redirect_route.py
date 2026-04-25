from flask import Blueprint, redirect, abort
from source.models.main_model import verify_code_exists
from source.services import redirect_service

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<code>", methods=["GET"])
def redirect_to_link(code: str) -> redirect:
    url_data = verify_code_exists(code)
    if url_data:
        redirect_service.add_new_click(code)
        return redirect(url_data[1])
    return abort(404)
