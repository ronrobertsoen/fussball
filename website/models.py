##Datenbankmodell #1.20.40
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))  # Ortschaft des Trainings/Spiels
    description = db.Column(db.String(255))
    event_type = db.Column(db.String(50))  # 'Training' oder 'Match'
    event_time = db.Column(db.DateTime(timezone=True), default=func.now())  # Zeitpunkt des Trainings/Spiels
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # ID des Trainers oder Erstellers
    zusagen = db.relationship('Zusage', back_populates='event')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(20), default='player')
    events = db.relationship('Event') #addiert user.id zu den events
    zusagen = db.relationship('Zusage', back_populates='user')
    

    def is_trainer(self):
        return self.role=='trainer'
    
class Zusage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    info = db.Column(db.String(50))
    status = db.Column(db.String(50))  # Beispielsweise 'zugesagt' oder 'abgesagt'

    user = db.relationship('User', back_populates='zusagen')
    event = db.relationship('Event', back_populates='zusagen')



