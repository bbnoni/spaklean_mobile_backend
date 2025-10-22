from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api')

USERS = {
    "admin@spaklean.com": {"password": "admin123", "role": "Admin"},
    "custodian@spaklean.com": {"password": "custodian123", "role": "Custodian"},
}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = USERS.get(email)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=8))
    return jsonify({"token": token, "role": user["role"], "email": email}), 200


@auth_bp.route('/scoreboard', methods=['GET'])
def scoreboard():
    data = [
        {"name": "John Doe", "score": 85, "category": "Facility Inspection"},
        {"name": "Mary Jane", "score": 90, "category": "Task Compliance"},
        {"name": "David Smith", "score": 75, "category": "Equipment Audit"},
    ]
    return jsonify({"ok": True, "data": data})
