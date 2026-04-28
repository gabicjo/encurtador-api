from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user
from source.services import auth_service
from source import error_handler

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["POST"])
def register():
    """
    Registra novo usuário.
    
    ---
    tags:
      - Autenticação
    summary: Registrar novo usuário
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
            - username
            - password
          properties:
            username:
              type: string
              example: joao
              description: Nome de usuário
            password:
              type: string
              example: senha123
              description: Senha do usuário
    responses:
      200:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: "Usuario criado com sucesso"
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            message:
              type: string
    """
    data = request.json
    
    try:
        if "username" in data and "password" in data:
            user = auth_service.register(data["username"], data["password"])
            return jsonify({"message": "Usuario criado com sucesso", "id": user.id})
        else:
            raise error_handler.SemURL("Username e password são obrigatórios")
    
    except error_handler.SemURL as e:
        return jsonify({"message": str(e)}), 400

    except error_handler.CodigoInvalido as e:
        return jsonify({"message": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Autentica usuário.
    
    ---
    tags:
      - Autenticação
    summary: Login de usuário
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
            - username
            - password
          properties:
            username:
              type: string
              example: joao
            password:
              type: string
              example: senha123
    responses:
      200:
        description: Login bem-sucedido
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: "Login bem-sucedido"
      401:
        description: Credenciais inválidas
        schema:
          type: object
          properties:
            message:
              type: string
    """
    data = request.json
    
    if "username" in data and "password" in data:
        user = auth_service.authenticate(data["username"], data["password"])
        if user:
            login_user(user)
            return jsonify({"message": "Login bem-sucedido"})
        else:
            return jsonify({"message": "Credenciais inválidas"}), 401
    
    return jsonify({"message": "Username e password são obrigatórios"}), 400


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Faz logout do usuário.
    
    Requer login.
    ---
    tags:
      - Autenticação
    summary: Logout de usuário
    produces:
      - application/json
    responses:
      200:
        description: Logout bem-sucedido
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: "Logout bem-sucedido"
    """
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"})