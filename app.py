from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
jwt = JWTManager(app)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Spaklean Backend API!"})

# Register Blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)
