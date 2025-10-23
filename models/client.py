from models import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    sector = db.relationship('Sector', backref='clients')
    location = db.relationship('Location', backref='clients')
