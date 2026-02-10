from datetime import datetime
from models import db

class Consultation(db.Model):
    """Model for storing video consultation information"""
    
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='scheduled')  # scheduled, active, completed, cancelled
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Consultation {self.room_id} - {self.doctor_name} with {self.patient_name}>'
    
    def to_dict(self):
        """Convert consultation object to dictionary"""
        return {
            'id': self.id,
            'room_id': self.room_id,
            'doctor_name': self.doctor_name,
            'patient_name': self.patient_name,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'status': self.status,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }
