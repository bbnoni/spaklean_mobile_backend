from models import db   # ✅ make sure this line is at the top
from datetime import datetime

# ----------------- Location Hierarchy Models -----------------

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sectors = db.relationship('Sector', backref='location', lazy=True)
    assignments = db.relationship('Assignment', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location {self.name}>"


class Sector(db.Model):
    __tablename__ = 'sectors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    categories = db.relationship('Category', backref='sector', lazy=True)
    assignments = db.relationship('Assignment', backref='sector', lazy=True)

    def __repr__(self):
        return f"<Sector {self.name}>"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'), nullable=False)

    rooms = db.relationship('Room', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    zone = db.Column(db.String(50))

    def __repr__(self):
        return f"<Room {self.name}>"


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Assignment user={self.user_id} loc={self.location_id}>"
