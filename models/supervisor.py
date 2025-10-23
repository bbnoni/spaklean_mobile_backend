from models import db

class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location', backref='supervisors')
