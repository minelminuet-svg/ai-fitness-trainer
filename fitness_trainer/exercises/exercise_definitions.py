"""Exercise definitions and metadata"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum


class ExerciseType(Enum):
    """Types of exercises supported"""
    ARM = "arm"
    LEG = "leg"
    CORE = "core"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    FULL_BODY = "full_body"


class DifficultyLevel(Enum):
    """Difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class AngleRequirement:
    """Joint angle requirement for an exercise position"""
    joint_name: str
    min_angle: float
    max_angle: float
    description: str


@dataclass
class ExercisePosition:
    """Represents a position in an exercise"""
    name: str
    description: str
    angle_requirements: List[AngleRequirement] = field(default_factory=list)
    duration: int = 0  # in frames/seconds, 0 = not timed
    visibility_threshold: float = 0.6


@dataclass
class Exercise:
    """Exercise definition"""
    id: str
    name: str
    description: str
    exercise_type: ExerciseType
    difficulty: DifficultyLevel
    positions: List[ExercisePosition]
    repetitions: int = 10
    sets: int = 3
    rest_period: int = 60  # seconds between sets
    target_muscles: List[str] = field(default_factory=list)
    equipment: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    
    def get_position(self, position_name: str) -> ExercisePosition:
        """Get a position by name"""
        for pos in self.positions:
            if pos.name == position_name:
                return pos
        raise ValueError(f"Position '{position_name}' not found in exercise '{self.name}'")


# Exercise definitions
BICEP_CURL = Exercise(
    id="bicep_curl",
    name="Bicep Curl",
    description="Classic arm exercise targeting biceps",
    exercise_type=ExerciseType.ARM,
    difficulty=DifficultyLevel.BEGINNER,
    target_muscles=["biceps", "forearms"],
    equipment=["dumbbells"],
    tips=[
        "Keep elbows at your sides",
        "Maintain a straight posture",
        "Control the movement, don't swing",
        "Full range of motion for best results",
    ],
    warnings=[
        "Do not swing the weights",
        "Keep core engaged",
    ],
    positions=[
        ExercisePosition(
            name="starting_position",
            description="Arms fully extended at sides",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=170,
                    max_angle=180,
                    description="Left arm fully extended"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=170,
                    max_angle=180,
                    description="Right arm fully extended"
                ),
            ],
        ),
        ExercisePosition(
            name="lifted_position",
            description="Arms lifted with elbows bent",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=40,
                    max_angle=90,
                    description="Left elbow bent"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=40,
                    max_angle=90,
                    description="Right elbow bent"
                ),
            ],
        ),
    ],
)

SQUAT = Exercise(
    id="squat",
    name="Squat",
    description="Lower body exercise targeting legs",
    exercise_type=ExerciseType.LEG,
    difficulty=DifficultyLevel.BEGINNER,
    repetitions=15,
    target_muscles=["quadriceps", "hamstrings", "glutes"],
    tips=[
        "Keep chest up",
        "Knees track over toes",
        "Weight in heels",
        "Full range of motion",
    ],
    warnings=[
        "Do not let knees cave inward",
        "Keep back straight",
    ],
    positions=[
        ExercisePosition(
            name="standing_position",
            description="Standing with feet shoulder-width apart",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_knee",
                    min_angle=160,
                    max_angle=180,
                    description="Left leg extended"
                ),
                AngleRequirement(
                    joint_name="right_knee",
                    min_angle=160,
                    max_angle=180,
                    description="Right leg extended"
                ),
            ],
        ),
        ExercisePosition(
            name="squat_position",
            description="Lowered squat position",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_knee",
                    min_angle=70,
                    max_angle=110,
                    description="Left knee bent to proper depth"
                ),
                AngleRequirement(
                    joint_name="right_knee",
                    min_angle=70,
                    max_angle=110,
                    description="Right knee bent to proper depth"
                ),
            ],
        ),
    ],
)

PUSH_UP = Exercise(
    id="push_up",
    name="Push Up",
    description="Upper body exercise targeting chest, shoulders, and triceps",
    exercise_type=ExerciseType.ARM,
    difficulty=DifficultyLevel.INTERMEDIATE,
    target_muscles=["chest", "shoulders", "triceps"],
    tips=[
        "Body straight from head to heels",
        "Elbows at 45 degree angle",
        "Full range of motion",
        "Controlled descent",
    ],
    warnings=[
        "Do not sag hips",
        "Keep neck neutral",
    ],
    positions=[
        ExercisePosition(
            name="top_position",
            description="Top of push up position",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=160,
                    max_angle=180,
                    description="Left arm extended"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=160,
                    max_angle=180,
                    description="Right arm extended"
                ),
            ],
        ),
        ExercisePosition(
            name="bottom_position",
            description="Bottom of push up position",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=70,
                    max_angle=90,
                    description="Left elbow bent"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=70,
                    max_angle=90,
                    description="Right elbow bent"
                ),
            ],
        ),
    ],
)

PLANK = Exercise(
    id="plank",
    name="Plank",
    description="Core exercise for stability and strength",
    exercise_type=ExerciseType.CORE,
    difficulty=DifficultyLevel.BEGINNER,
    repetitions=1,
    duration=30,  # 30 seconds
    target_muscles=["core", "shoulders"],
    tips=[
        "Keep body straight",
        "Engage core muscles",
        "Breathe steadily",
        "Build duration gradually",
    ],
    warnings=[
        "Do not sag hips",
        "Do not raise hips too high",
    ],
    positions=[
        ExercisePosition(
            name="plank_position",
            description="Straight body position",
            angle_requirements=[
                AngleRequirement(
                    joint_name="body_alignment",
                    min_angle=170,
                    max_angle=180,
                    description="Body straight from head to heels"
                ),
            ],
            duration=30,
        ),
    ],
)

SHOULDER_PRESS = Exercise(
    id="shoulder_press",
    name="Shoulder Press",
    description="Shoulder exercise using dumbbells",
    exercise_type=ExerciseType.ARM,
    difficulty=DifficultyLevel.INTERMEDIATE,
    target_muscles=["shoulders", "triceps"],
    equipment=["dumbbells"],
    tips=[
        "Keep core tight",
        "Full range of motion",
        "Controlled movement",
        "Single arm or both",
    ],
    warnings=[
        "Do not arch back excessively",
        "Maintain stability",
    ],
    positions=[
        ExercisePosition(
            name="starting_position",
            description="Dumbbells at shoulder height",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=80,
                    max_angle=100,
                    description="Left elbow at 90 degrees"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=80,
                    max_angle=100,
                    description="Right elbow at 90 degrees"
                ),
            ],
        ),
        ExercisePosition(
            name="pressed_position",
            description="Arms fully extended overhead",
            angle_requirements=[
                AngleRequirement(
                    joint_name="left_elbow",
                    min_angle=170,
                    max_angle=180,
                    description="Left arm extended"
                ),
                AngleRequirement(
                    joint_name="right_elbow",
                    min_angle=170,
                    max_angle=180,
                    description="Right arm extended"
                ),
            ],
        ),
    ],
)

# Registry of all exercises
EXERCISE_REGISTRY: Dict[str, Exercise] = {
    BICEP_CURL.id: BICEP_CURL,
    SQUAT.id: SQUAT,
    PUSH_UP.id: PUSH_UP,
    PLANK.id: PLANK,
    SHOULDER_PRESS.id: SHOULDER_PRESS,
}


def get_exercise(exercise_id: str) -> Exercise:
    """Get exercise by ID"""
    if exercise_id not in EXERCISE_REGISTRY:
        raise ValueError(f"Exercise '{exercise_id}' not found")
    return EXERCISE_REGISTRY[exercise_id]


def list_exercises(exercise_type: ExerciseType = None, 
                   difficulty: DifficultyLevel = None) -> List[Exercise]:
    """List exercises with optional filtering"""
    exercises = list(EXERCISE_REGISTRY.values())
    
    if exercise_type:
        exercises = [e for e in exercises if e.exercise_type == exercise_type]
    
    if difficulty:
        exercises = [e for e in exercises if e.difficulty == difficulty]
    
    return exercises
