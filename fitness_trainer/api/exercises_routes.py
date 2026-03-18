"""Flask API Routes for Exercises"""
from flask import Blueprint, jsonify, request
from ..exercises import get_exercise, list_exercises, ExerciseType, DifficultyLevel

exercises_bp = Blueprint('exercises', __name__, url_prefix='/api/exercises')


@exercises_bp.route('/types', methods=['GET'])
def get_exercise_types():
    """Get all exercise types"""
    types = [e.value for e in ExerciseType]
    return jsonify({
        'success': True,
        'types': types
    })


@exercises_bp.route('/difficulties', methods=['GET'])
def get_difficulty_levels():
    """Get all difficulty levels"""
    difficulties = [d.value for d in DifficultyLevel]
    return jsonify({
        'success': True,
        'difficulties': difficulties
    })


@exercises_bp.route('/', methods=['GET'])
def get_all_exercises():
    """Get all available exercises with optional filtering"""
    exercise_type = request.args.get('type')
    difficulty = request.args.get('difficulty')
    
    try:
        # Parse filters if provided
        type_filter = None
        difficulty_filter = None
        
        if exercise_type:
            type_filter = ExerciseType(exercise_type)
        if difficulty:
            difficulty_filter = DifficultyLevel(difficulty)
        
        exercises = list_exercises(type_filter, difficulty_filter)
        
        return jsonify({
            'success': True,
            'count': len(exercises),
            'exercises': [
                {
                    'id': e.id,
                    'name': e.name,
                    'description': e.description,
                    'type': e.exercise_type.value,
                    'difficulty': e.difficulty.value,
                    'target_muscles': e.target_muscles,
                    'equipment': e.equipment,
                    'repetitions': e.repetitions,
                    'sets': e.sets,
                }
                for e in exercises
            ]
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@exercises_bp.route('/<exercise_id>', methods=['GET'])
def get_exercise_details(exercise_id):
    """Get detailed information about a specific exercise"""
    try:
        exercise = get_exercise(exercise_id)
        
        return jsonify({
            'success': True,
            'exercise': {
                'id': exercise.id,
                'name': exercise.name,
                'description': exercise.description,
                'type': exercise.exercise_type.value,
                'difficulty': exercise.difficulty.value,
                'target_muscles': exercise.target_muscles,
                'equipment': exercise.equipment,
                'repetitions': exercise.repetitions,
                'sets': exercise.sets,
                'rest_period': exercise.rest_period,
                'tips': exercise.tips,
                'warnings': exercise.warnings,
                'positions': [
                    {
                        'name': pos.name,
                        'description': pos.description,
                        'duration': pos.duration,
                    }
                    for pos in exercise.positions
                ]
            }
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@exercises_bp.route('/types', methods=['GET'])
def get_exercise_types():
    """Get all exercise types"""
    types = [e.value for e in ExerciseType]
    return jsonify({
        'success': True,
        'types': types
    })


@exercises_bp.route('/difficulties', methods=['GET'])
def get_difficulty_levels():
    """Get all difficulty levels"""
    difficulties = [d.value for d in DifficultyLevel]
    return jsonify({
        'success': True,
        'difficulties': difficulties
    })
