from flask import Flask
from flask_cors import CORS
from source.routes.encurtar_route import encurtar_bp
from source.routes.redirect_route import redirect_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(encurtar_bp)
app.register_blueprint(redirect_bp)


app.run(port="9284")