"""Exercises Module
Exercise definitions, validation, and feedback"""

from .exercise_definitions import (
    Exercise,
    ExerciseType,
    DifficultyLevel,
    ExercisePosition,
    AngleRequirement,
    get_exercise,
    list_exercises,
)
from .exercise_validator import (
    ExerciseValidator,
    ValidationResult,
    RepetitionCounter,
    FormFeedbackEngine,
)

__all__ = [
    'Exercise',
    'ExerciseType',
    'DifficultyLevel',
    'ExercisePosition',
    'AngleRequirement',
    'get_exercise',
    'list_exercises',
    'ExerciseValidator',
    'ValidationResult',
    'RepetitionCounter',
    'FormFeedbackEngine',
]
