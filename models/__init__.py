from flask_sqlalchemy import SQLAlchemy
from .location import Location, Sector, Category, Room, Assignment


db = SQLAlchemy()
