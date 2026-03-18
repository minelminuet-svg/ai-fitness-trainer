"""Flask API Routes for Training Sessions"""
from flask import Blueprint, jsonify, request
from datetime import datetime
from ..exercises import get_exercise, ExerciseValidator, FormFeedbackEngine
import json

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

# In-memory storage for sessions (in production, use database)
active_sessions = {}


@sessions_bp.route('/', methods=['POST'])
def create_session():
    """Create a new training session"""
    data = request.get_json()
    
    try:
        exercise_id = data.get('exercise_id')
        exercise = get_exercise(exercise_id)
        
        session_id = f"session_{int(datetime.now().timestamp() * 1000)}"
        
        session_data = {
            'id': session_id,
            'exercise_id': exercise_id,
            'exercise_name': exercise.name,
            'started_at': datetime.now().isoformat(),
            'reps': 0,
            'sets': 0,
            'current_position': 'starting_position',
            'form_score': 0.0,
            'duration': 0,
            'status': 'active',
        }
        
        active_sessions[session_id] = session_data
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'exercise': {
                'id': exercise.id,
                'name': exercise.name,
                'target_reps': exercise.repetitions,
                'target_sets': exercise.sets,
            }
        }), 201
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sessions_bp.route('/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get current session status"""
    if session_id not in active_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    session_data = active_sessions[session_id]
    
    return jsonify({
        'success': True,
        'session': session_data
    })


@sessions_bp.route('/<session_id>/update', methods=['POST'])
def update_session(session_id):
    """Update session with current pose data"""
    if session_id not in active_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    data = request.get_json()
    
    try:
        session_data = active_sessions[session_id]
        
        # Update session with pose data
        if 'reps' in data:
            session_data['reps'] = data['reps']
        if 'sets' in data:
            session_data['sets'] = data['sets']
        if 'form_score' in data:
            session_data['form_score'] = data['form_score']
        if 'current_position' in data:
            session_data['current_position'] = data['current_position']
        if 'duration' in data:
            session_data['duration'] = data['duration']
        
        return jsonify({
            'success': True,
            'session': session_data
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sessions_bp.route('/<session_id>/end', methods=['POST'])
def end_session(session_id):
    """End a training session"""
    if session_id not in active_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    session_data = active_sessions[session_id]
    session_data['status'] = 'completed'
    session_data['ended_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'session': session_data,
        'message': 'Session ended successfully'
    })
