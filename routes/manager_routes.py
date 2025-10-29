from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Location, Sector, Category, Room, Assignment

manager_bp = Blueprint('manager_bp', __name__)

@manager_bp.route("/manager/locations/<int:user_id>")
@jwt_required()
def get_manager_locations(user_id):
    current_user_id = get_jwt_identity()
    print(f"🔹 Authenticated user ID: {current_user_id}, Requested ID: {user_id}")

    if current_user_id != user_id:
        return jsonify({"error": "Token mismatch"}), 403

    user = User.query.get(user_id)
    if not user or user.role != "Custodial Manager":
        return jsonify({"error": "Unauthorized"}), 403

    assignments = Assignment.query.filter_by(user_id=user.id).all()
    data = []

    for a in assignments:
        location = Location.query.get(a.location_id)
        if not location:
            continue

        sectors = [
            {
                "name": s.name,
                "categories": [
                    {
                        "name": c.name,
                        "rooms": [{"name": r.name} for r in c.rooms],
                    }
                    for c in s.categories
                ],
            }
            for s in location.sectors
        ]
        data.append({"name": location.name, "sectors": sectors})

    return jsonify(data)
