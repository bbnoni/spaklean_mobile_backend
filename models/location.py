from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create local reference to db (initialized in __init__.py)
db = SQLAlchemy()

# ----------------- Location Hierarchy Models -----------------

# Main Location Table (e.g., Aviation, Freezones)
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sectors = db.relationship('Sector', backref='location', lazy=True)
    assignments = db.relationship('Assignment', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location {self.name}>"


# Sector Table (e.g., Airlines, Banking, Health)
class Sector(db.Model):
    __tablename__ = 'sectors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    categories = db.relationship('Category', backref='sector', lazy=True)
    assignments = db.relationship('Assignment', backref='sector', lazy=True)

    def __repr__(self):
        return f"<Sector {self.name}>"


# Category Table (e.g., Ghana Airport Company, Delta, Tap Portugal)
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'), nullable=False)

    rooms = db.relationship('Room', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


# Room Table (e.g., A1, A2, Delta Airport Office)
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f"<Room {self.name}>"


# Assignment Table (maps users to locations/sectors)
class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Assignment user={self.user_id} loc={self.location_id}>"
