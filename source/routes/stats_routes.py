from flask import Blueprint, request, jsonify, redirect, abort
from source import error_handler
from source.services import stats_service

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats/<code>", methods=["GET"])
def get_url_stats(code: str) -> dict:
    try:
        stats = stats_service.get_url_stats(code)
        return jsonify(stats)
        
    except error_handler.CodigoInvalido as e:
        return jsonify({"message": str(e)}), 404