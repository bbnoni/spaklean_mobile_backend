# models/supervisor_assignment.py
from models import db

class SupervisorAssignment(db.Model):
    __tablename__ = 'supervisor_assignments'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    manager = db.relationship("User", foreign_keys=[manager_id])
    supervisor = db.relationship("User", foreign_keys=[supervisor_id])
