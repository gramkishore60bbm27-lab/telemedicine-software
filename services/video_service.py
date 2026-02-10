import uuid
import logging
from datetime import datetime
from models import db
from models.consultation import Consultation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoService:
    """Service class for managing video consultation rooms"""
    
    @staticmethod
    def generate_room_id():
        """Generate a secure unique room ID using UUID4"""
        return str(uuid.uuid4())
    
    @staticmethod
    def create_consultation(doctor_name, patient_name, scheduled_time=None):
        """
        Create a new video consultation room
        
        Args:
            doctor_name: Name of the doctor
            patient_name: Name of the patient
            scheduled_time: Optional scheduled time (defaults to now)
        
        Returns:
            dict: Consultation details including room_id
        """
        try:
            room_id = VideoService.generate_room_id()
            
            if scheduled_time is None:
                scheduled_time = datetime.utcnow()
            
            consultation = Consultation(
                room_id=room_id,
                doctor_name=doctor_name,
                patient_name=patient_name,
                scheduled_time=scheduled_time,
                status='scheduled'
            )
            
            db.session.add(consultation)
            db.session.commit()
            
            logger.info(f"Created consultation room: {room_id} for {doctor_name} with {patient_name}")
            
            return {
                'success': True,
                'consultation': consultation.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating consultation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_consultation(room_id):
        """
        Get consultation details by room ID
        
        Args:
            room_id: The unique room identifier
        
        Returns:
            dict: Consultation details or error
        """
        try:
            consultation = Consultation.query.filter_by(room_id=room_id).first()
            
            if not consultation:
                return {
                    'success': False,
                    'error': 'Consultation not found'
                }
            
            return {
                'success': True,
                'consultation': consultation.to_dict()
            }
        except Exception as e:
            logger.error(f"Error retrieving consultation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def validate_room_access(room_id):
        """
        Validate if a room exists and is accessible
        
        Args:
            room_id: The unique room identifier
        
        Returns:
            bool: True if room is valid and accessible
        """
        try:
            consultation = Consultation.query.filter_by(room_id=room_id).first()
            
            if not consultation:
                return False
            
            # Room is accessible if it's scheduled or active
            if consultation.status in ['scheduled', 'active']:
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error validating room access: {str(e)}")
            return False
    
    @staticmethod
    def join_consultation(room_id):
        """
        Mark consultation as active when someone joins
        
        Args:
            room_id: The unique room identifier
        
        Returns:
            dict: Updated consultation details
        """
        try:
            consultation = Consultation.query.filter_by(room_id=room_id).first()
            
            if not consultation:
                return {
                    'success': False,
                    'error': 'Consultation not found'
                }
            
            if consultation.status == 'scheduled':
                consultation.status = 'active'
                db.session.commit()
                logger.info(f"Consultation {room_id} marked as active")
            
            return {
                'success': True,
                'consultation': consultation.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error joining consultation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def end_consultation(room_id):
        """
        End a consultation and mark it as completed
        
        Args:
            room_id: The unique room identifier
        
        Returns:
            dict: Result of the operation
        """
        try:
            consultation = Consultation.query.filter_by(room_id=room_id).first()
            
            if not consultation:
                return {
                    'success': False,
                    'error': 'Consultation not found'
                }
            
            consultation.status = 'completed'
            consultation.ended_at = datetime.utcnow()
            
            # Calculate duration if consultation was active
            if consultation.scheduled_time:
                duration = (datetime.utcnow() - consultation.scheduled_time).total_seconds() / 60
                consultation.duration = int(duration)
            
            db.session.commit()
            logger.info(f"Consultation {room_id} ended. Duration: {consultation.duration} minutes")
            
            return {
                'success': True,
                'consultation': consultation.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error ending consultation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_active_consultations():
        """
        Get list of all active consultations
        
        Returns:
            list: List of active consultation dictionaries
        """
        try:
            consultations = Consultation.query.filter(
                Consultation.status.in_(['scheduled', 'active'])
            ).order_by(Consultation.scheduled_time.desc()).all()
            
            return {
                'success': True,
                'consultations': [c.to_dict() for c in consultations]
            }
        except Exception as e:
            logger.error(f"Error retrieving active consultations: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'consultations': []
            }
