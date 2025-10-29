from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.user import User
from models import db

auth_bp = Blueprint('auth_bp', __name__)

# ---------------- REGISTER ROUTE ----------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input fields
    if not data or not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409

    # Create new user
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()

    print(f"✅ New user registered: {user.email}")

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN ROUTE ----------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Validate credentials
    if not user or not check_password_hash(user.password_hash, password):
        print(f"❌ Failed login attempt for {email}")
        return jsonify({"error": "Invalid email or password"}), 401

    # ✅ PyJWT 2.x requires 'sub' (identity) as a string
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=8)
    )

    print(f"🔐 Login successful for {user.email} (Role: {user.role})")
    print(f"🔹 Generated JWT for user_id={user.id}")

    # ✅ Return full user details to Flutter
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": user.role,
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }), 200
