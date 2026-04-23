from flask import Blueprint, request, jsonify

encurtar_bp = Blueprint("encurtar", __name__)

@encurtar_bp.route("/encurtar", methods=["POST"])
def generate_code():
    data = request.json

    if "url" in data and data['url'] not in [None, ""]:
        return jsonify({"message": "ok"})
    return jsonify({"message": "error"}), 400