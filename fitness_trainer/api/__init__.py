"""API Module - Flask REST API for AI Fitness Trainer"""

from .exercises_routes import exercises_bp
from .sessions_routes import sessions_bp
from .analysis_routes import analysis_bp

__all__ = [
    'exercises_bp',
    'sessions_bp',
    'analysis_bp',
]
