from flask import Blueprint, request, jsonify
from models import db
from models.inspection import InspectionTask

inspection_bp = Blueprint("inspection_bp", __name__)

@inspection_bp.route("/api/tasks/submit", methods=["POST"])
def submit_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        # ✅ Handle "null" or empty strings safely
        room_id = data.get("room_id")
        if isinstance(room_id, str) and room_id.lower() == "null":
            room_id = None

        done_on_behalf_user_id = data.get("done_on_behalf_user_id")
        if isinstance(done_on_behalf_user_id, str) and done_on_behalf_user_id.lower() == "null":
            done_on_behalf_user_id = None

        # ✅ Create the record safely
        task = InspectionTask(
            user_id=data.get("user_id"),
            done_on_behalf_user_id=done_on_behalf_user_id,
            room_id=room_id,
            zone_name=data.get("zone_name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            location_name=data.get("location_name"),
            area_scores=data.get("area_scores"),
            zone_score=data.get("zone_score"),
            facility_score=data.get("facility_score"),
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({"message": "Inspection task saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in submit_task: {e}")
        return jsonify({"error": str(e)}), 500
