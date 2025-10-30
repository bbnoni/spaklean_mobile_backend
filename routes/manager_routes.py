from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Location, Sector, Category, Room, Assignment

manager_bp = Blueprint('manager_bp', __name__)

# ---------------- ALL LOCATIONS (GROUPED BY ZONE) ----------------
@manager_bp.route("/manager/locations/<int:user_id>")
@jwt_required()
def get_manager_locations(user_id):
    try:
        current_user_id = int(get_jwt_identity())
        print(f"🔹 Token identity = {current_user_id}, requested user_id = {user_id}")

        # Validate user and role
        if current_user_id != user_id:
            return jsonify({"error": "Forbidden: token/user mismatch"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "Custodial Manager":
            return jsonify({"error": "Unauthorized"}), 403

        # Get assigned locations for this manager
        assignments = Assignment.query.filter_by(user_id=user.id).all()
        data = []

        for a in assignments:
            location = Location.query.get(a.location_id)
            if not location:
                continue

            # Group rooms by zone
            zones = {}
            for sector in location.sectors:
                for category in sector.categories:
                    for room in category.rooms:
                        zone_name = room.zone or "Unassigned Zone"
                        if zone_name not in zones:
                            zones[zone_name] = []
                        zones[zone_name].append({
                            "room_name": room.name,
                            "sector": sector.name,
                            "category": category.name
                        })

            # Append structured data for this location
            data.append({
                "location": location.name,
                "zones": [
                    {"zone_name": zone, "rooms": zones[zone]}
                    for zone in zones.keys()
                ]
            })

        return jsonify(data), 200

    except Exception as e:
        print(f"❌ Exception in manager route: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------- FILTER BY SPECIFIC ZONE ----------------

@manager_bp.route("/manager/locations/<int:user_id>/zone/<string:zone>")
@jwt_required()
def get_rooms_by_zone(user_id, zone):
    try:
        current_user_id = int(get_jwt_identity())
        print(f"🔹 Token identity = {current_user_id}, requested user_id = {user_id}, zone = {zone}")

        # Validate user and role##
        if current_user_id != user_id:
            return jsonify({"error": "Forbidden: token/user mismatch"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "Custodial Manager":
            return jsonify({"error": "Unauthorized"}), 403

        assignments = Assignment.query.filter_by(user_id=user.id).all()
        grouped_data = {}

        for a in assignments:
            location = Location.query.get(a.location_id)
            if not location:
                continue

            for sector in location.sectors:
                for category in sector.categories:
                    for room in category.rooms:
                        if room.zone and room.zone.lower() == zone.lower():
                            grouped_data.setdefault(location.name, {}) \
                                .setdefault(sector.name, []) \
                                .append({
                                    "room_name": room.name,
                                    "category": category.name,
                                    "zone": room.zone
                                })

        print(f"✅ Returning grouped data for zone '{zone}': {len(grouped_data)} locations found.")
        return jsonify(grouped_data), 200

    except Exception as e:
        print(f"❌ Exception in get_rooms_by_zone: {e}")
        return jsonify({"error": str(e)}), 500
