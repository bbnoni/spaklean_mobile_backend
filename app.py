from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import datetime

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "spaklean_secret_key"
jwt = JWTManager(app)

# Dummy users for testing purposes
# Dummy users for testing purposes
USERS = {
    "admin@spaklean.com": {"password": "admin123", "role": "Admin"},
    "custodian@spaklean.com": {"password": "custodian123", "role": "Custodian"},
}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Spaklean Backend API!"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = USERS.get(email)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=email, expires_delta=datetime.timedelta(hours=8)
    )
    return jsonify({"token": access_token, "role": user["role"], "email": email}), 200


@app.route("/api/scoreboard", methods=["GET"])
@jwt_required()
def scoreboard():
    # Dummy data
    data = [
        {"name": "John Doe", "score": 85, "category": "Facility Inspection"},
        {"name": "Mary Jane", "score": 90, "category": "Task Compliance"},
        {"name": "David Smith", "score": 75, "category": "Equipment Audit"},
    ]
    return jsonify({"ok": True, "data": data})


@app.route("/api/admin/offices", methods=["GET", "POST"])
@jwt_required()
def manage_offices():
    current_user = get_jwt_identity()
    user_role = USERS.get(current_user, {}).get("role")

    if user_role != "Admin":
        return jsonify({"error": "Unauthorized"}), 403

    if request.method == "POST":
        data = request.get_json()
        office_name = data.get("name")
        return jsonify({"message": f"Office '{office_name}' created successfully."})

    offices = [
        {"id": 1, "name": "Head Office"},
        {"id": 2, "name": "Accra North"},
        {"id": 3, "name": "Freezones"},
    ]
    return jsonify({"offices": offices})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
