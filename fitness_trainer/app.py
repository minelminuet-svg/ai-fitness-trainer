"""Main entry point for AI Fitness Trainer"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import DEBUG, PORT, HOST
from api import exercises_bp, sessions_bp, analysis_bp

app = Flask(__name__)
CORS(app)

# Register API blueprints
app.register_blueprint(exercises_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(analysis_bp)


@app.route('/')
def index():
    return jsonify({
        'message': 'AI Fitness Trainer API',
        'version': '1.0',
        'endpoints': {
            'exercises': '/api/exercises',
            'sessions': '/api/sessions',
            'analysis': '/api/analysis',
            'health': '/health',
        }
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
