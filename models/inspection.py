from datetime import datetime
from models import db

class InspectionTask(db.Model):
    __tablename__ = "inspection_tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)               # user performing inspection
    done_on_behalf_user_id = db.Column(db.Integer, nullable=True) # optional
    #room_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    zone_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_name = db.Column(db.String(255))
    area_scores = db.Column(db.JSON)
    zone_score = db.Column(db.Float)
    facility_score = db.Column(db.Float)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<InspectionTask room_id={self.room_id} user_id={self.user_id}>"
