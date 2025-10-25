from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
from routes.auth_routes import auth_bp

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize Database, Migration, and JWT
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Spaklean Backend API!"})

# Register Blueprints
app.register_blueprint(auth_bp)

# Entry Point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
