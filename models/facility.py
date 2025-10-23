from models import db

class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.id'))
    client = db.relationship('Client', backref='facilities')
    supervisor = db.relationship('Supervisor', backref='facilities')
