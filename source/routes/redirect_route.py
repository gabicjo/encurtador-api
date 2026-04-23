from flask import Blueprint, request, jsonify, redirect, abort
from source import error_handler
from source.models.main_model import verify_code_exists

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<code>", methods=["GET"])
def redirect_to_link(code):
    url_data = verify_code_exists(code)
    if url_data:
        return redirect(url_data[1])
    return abort(404)