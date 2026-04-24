from flask import Flask
from flask_cors import CORS
from source.routes.encurtar_route import encurtar_bp
from source.routes.redirect_route import redirect_bp
from source.models.main_model import criar_tabela

app = Flask(__name__)
CORS(app)

criar_tabela()

app.register_blueprint(encurtar_bp)
app.register_blueprint(redirect_bp)


app.run(port="9284", debug=True)