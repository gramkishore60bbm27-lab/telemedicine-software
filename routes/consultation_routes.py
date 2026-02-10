from flask import Blueprint, request, jsonify
from services.video_service import VideoService
from datetime import datetime

# Create Blueprint for consultation routes
consultation_bp = Blueprint('consultation', __name__, url_prefix='/api/consultation')

@consultation_bp.route('/create', methods=['POST'])
def create_consultation():
    """
    Create a new video consultation room
    
    Expected JSON body:
    {
        "doctor_name": "Dr. Smith",
        "patient_name": "John Doe",
        "scheduled_time": "2024-01-01T10:00:00" (optional)
    }
    
    Returns:
        JSON response with consultation details including room_id
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        doctor_name = data.get('doctor_name')
        patient_name = data.get('patient_name')
        scheduled_time_str = data.get('scheduled_time')
        
        if not doctor_name or not patient_name:
            return jsonify({
                'success': False,
                'error': 'Doctor name and patient name are required'
            }), 400
        
        # Parse scheduled time if provided
        scheduled_time = None
        if scheduled_time_str:
            try:
                scheduled_time = datetime.fromisoformat(scheduled_time_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid scheduled_time format. Use ISO format.'
                }), 400
        
        result = VideoService.create_consultation(doctor_name, patient_name, scheduled_time)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@consultation_bp.route('/<room_id>', methods=['GET'])
def get_consultation(room_id):
    """
    Get consultation room details
    
    Args:
        room_id: The unique room identifier
    
    Returns:
        JSON response with consultation details
    """
    try:
        result = VideoService.get_consultation(room_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@consultation_bp.route('/join', methods=['POST'])
def join_consultation():
    """
    Validate and join a consultation room
    
    Expected JSON body:
    {
        "room_id": "uuid-room-id"
    }
    
    Returns:
        JSON response with validation result and consultation details
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        room_id = data.get('room_id')
        
        if not room_id:
            return jsonify({
                'success': False,
                'error': 'Room ID is required'
            }), 400
        
        # Validate room access
        if not VideoService.validate_room_access(room_id):
            return jsonify({
                'success': False,
                'error': 'Invalid or inactive consultation room'
            }), 404
        
        # Mark consultation as active
        result = VideoService.join_consultation(room_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@consultation_bp.route('/active', methods=['GET'])
def get_active_consultations():
    """
    Get list of all active consultations
    
    Returns:
        JSON response with list of active consultations
    """
    try:
        result = VideoService.get_active_consultations()
        return jsonify(result), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'consultations': []
        }), 500

@consultation_bp.route('/end', methods=['POST'])
def end_consultation():
    """
    End a consultation and mark it as completed
    
    Expected JSON body:
    {
        "room_id": "uuid-room-id"
    }
    
    Returns:
        JSON response with updated consultation details
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        room_id = data.get('room_id')
        
        if not room_id:
            return jsonify({
                'success': False,
                'error': 'Room ID is required'
            }), 400
        
        result = VideoService.end_consultation(room_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500
