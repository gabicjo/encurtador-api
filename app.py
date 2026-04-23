from flask import Flask
from flask_cors import CORS
from source.routes.encurtar_route import encurtar_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(encurtar_bp)

app.run(debug=True, port="9284")