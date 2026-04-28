import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
from source.routes.encurtar_route import encurtar_bp
from source.routes.redirect_route import redirect_bp
from source.routes.stats_routes import stats_bp
from source.routes.auth_routes import auth_bp
from source.models.main_model import criar_tabela
from source.models.users_model import criar_tabela_users
from source.auth import login_manager

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

CORS(app)
Swagger(app)

# Login Manager
login_manager.init_app(app)

# Criar tabelas
criar_tabela()
criar_tabela_users()

app.register_blueprint(encurtar_bp)
app.register_blueprint(redirect_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(auth_bp)

app.run(port="9284")