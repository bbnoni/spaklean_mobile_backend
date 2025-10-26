from flask_sqlalchemy import SQLAlchemy

# Create ONE shared SQLAlchemy instance
db = SQLAlchemy()

# Import models AFTER db is created to avoid circular imports
from .user import User
from .location import Location, Sector, Category, Room, Assignment
