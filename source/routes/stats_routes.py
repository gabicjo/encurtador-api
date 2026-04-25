from flask import Blueprint, request, jsonify, redirect, abort
from source import error_handler

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats/<code>", methods=["GET"])
def get_url_stats(code):
    