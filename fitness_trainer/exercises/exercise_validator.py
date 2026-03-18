"""Exercise validation and form checking"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .exercise_definitions import Exercise, ExercisePosition, AngleRequirement


@dataclass
class ValidationResult:
    """Result of exercise form validation"""
    is_valid: bool
    score: float  # 0.0 to 1.0
    passed_checks: List[str]
    failed_checks: List[str]
    feedback: List[str]
    warnings: List[str]


class ExerciseValidator:
    """Validates exercise form and provides feedback"""
    
    def __init__(self, exercise: Exercise):
        """Initialize validator for an exercise"""
        self.exercise = exercise
        self.angle_tolerance = 15  # degrees
        
    def validate_position(self, detector, target_position: ExercisePosition) -> ValidationResult:
        """Validate if pose matches target exercise position
        
        Args:
            detector: PoseDetector instance with current pose
            target_position: Target ExercisePosition to validate against
            
        Returns:
            ValidationResult with validation details
        """
        passed_checks = []
        failed_checks = []
        feedback = []
        warnings = []
        
        # Check all angle requirements
        for requirement in target_position.angle_requirements:
            result = self._check_angle_requirement(detector, requirement)
            if result['passed']:
                passed_checks.append(result['description'])
            else:
                failed_checks.append(result['description'])
                feedback.append(result['feedback'])
        
        # Check visibility of joints
        visibility_checks = self._check_joint_visibility(detector, target_position)
        if visibility_checks['passed']:
            passed_checks.append("All joints visible")
        else:
            failed_checks.append("Some joints not visible")
            feedback.append("Could not see all body parts clearly")
        
        # Calculate overall score
        total_checks = len(target_position.angle_requirements)
        passed_angle_checks = sum(
            1 for req in target_position.angle_requirements
            if self._check_angle_requirement(detector, req)['passed']
        )
        
        score = passed_angle_checks / total_checks if total_checks > 0 else 0.0
        is_valid = score >= 0.7  # 70% or better
        
        # Add exercise-specific warnings
        for warning in self.exercise.warnings:
            warnings.append(warning)
        
        return ValidationResult(
            is_valid=is_valid,
            score=score,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            feedback=feedback,
            warnings=warnings,
        )
    
    def _check_angle_requirement(self, detector, requirement: AngleRequirement) -> Dict:
        """Check a single angle requirement"""
        # Map joint names to proper landmark identifiers
        joint_map = {
            'left_elbow': ('LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'),
            'right_elbow': ('RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST'),
            'left_knee': ('LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'),
            'right_knee': ('RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'),
            'left_hip': ('LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE'),
            'right_hip': ('RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE'),
            'left_shoulder': ('NOSE', 'LEFT_SHOULDER', 'LEFT_ELBOW'),
            'right_shoulder': ('NOSE', 'RIGHT_SHOULDER', 'RIGHT_ELBOW'),
            'body_alignment': ('NOSE', 'NECK', 'HIPS'),
        }
        
        joint_name = requirement.joint_name.lower()
        if joint_name not in joint_map:
            return {
                'passed': False,
                'description': f"Unknown joint: {requirement.joint_name}",
                'feedback': f"Cannot validate unknown joint {requirement.joint_name}",
            }
        
        joint_start, joint_center, joint_end = joint_map[joint_name]
        angle = detector.get_joint_angle(joint_start, joint_center, joint_end)
        
        if angle is None:
            return {
                'passed': False,
                'description': f"Could not measure {requirement.joint_name}",
                'feedback': f"Cannot detect {requirement.joint_name}",
            }
        
        in_range = requirement.min_angle <= angle <= requirement.max_angle
        
        return {
            'passed': in_range,
            'description': f"{requirement.joint_name}: {angle:.1f}°",
            'feedback': requirement.description if in_range else f"Adjust {requirement.joint_name} (target: {requirement.min_angle}°-{requirement.max_angle}°, current: {angle:.1f}°)",
            'angle': angle,
        }
    
    def _check_joint_visibility(self, detector, position: ExercisePosition) -> Dict:
        """Check if all required joints are visible with sufficient confidence"""
        landmarks = detector.get_all_landmarks()
        
        visible_count = sum(1 for p in landmarks.values() if p.visibility >= position.visibility_threshold)
        min_visible = len(landmarks) * position.visibility_threshold
        
        return {
            'passed': visible_count >= min_visible * 0.8,  # 80% of landmarks should be visible
            'visible_count': visible_count,
            'required': min_visible,
        }
    
    def validate_sequence(self, detector, positions: List[ExercisePosition]) -> List[ValidationResult]:
        """Validate a sequence of positions (e.g., full rep)
        
        Args:
            detector: PoseDetector instance
            positions: List of positions to validate in sequence
            
        Returns:
            List of ValidationResult for each position
        """
        results = []
        for position in positions:
            result = self.validate_position(detector, position)
            results.append(result)
        return results
    
    def get_exercise_tips(self) -> List[str]:
        """Get tips for performing this exercise"""
        return self.exercise.tips
    
    def get_exercise_warnings(self) -> List[str]:
        """Get safety warnings for this exercise"""
        return self.exercise.warnings


class RepetitionCounter:
    """Tracks and counts exercise repetitions"""
    
    def __init__(self, exercise: Exercise):
        """Initialize repetition counter"""
        self.exercise = exercise
        self.rep_count = 0
        self.set_count = 0
        self.in_rep = False
        self.state_history = []
        self.rep_states = []  # Track which state each rep is in
        
    def update(self, validation_result: ValidationResult, position_type: str) -> Dict:
        """Update rep counter based on validation result
        
        Args:
            validation_result: Current validation result
            position_type: Type of position ('starting', 'lifted', 'bottom', etc.)
            
        Returns:
            Dictionary with current count and rep status
        """
        status = {
            'rep_count': self.rep_count,
            'set_count': self.set_count,
            'in_rep': self.in_rep,
            'rep_completed': False,
        }
        
        # Track state transitions
        if validation_result.is_valid:
            if not self.in_rep and position_type in ['lifted_position', 'squat_position', 'bottom_position']:
                self.in_rep = True
            elif self.in_rep and position_type in ['starting_position', 'standing_position', 'top_position']:
                self.in_rep = False
                self.rep_count += 1
                status['rep_completed'] = True
                
                # Check if set is complete
                if self.rep_count >= self.exercise.repetitions:
                    self.set_count += 1
                    self.rep_count = 0
                    status['set_completed'] = True
        
        status['rep_count'] = self.rep_count
        status['set_count'] = self.set_count
        
        return status
    
    def reset_rep(self):
        """Reset current rep"""
        self.rep_count = 0
        self.in_rep = False
    
    def reset_set(self):
        """Reset current set"""
        self.set_count += 1
        self.rep_count = 0
        self.in_rep = False
    
    def reset_all(self):
        """Reset all counts"""
        self.rep_count = 0
        self.set_count = 0
        self.in_rep = False


class FormFeedbackEngine:
    """Generates real-time feedback on exercise form"""
    
    FEEDBACK_PRIORITY = {
        'critical': 3,
        'warning': 2,
        'tip': 1,
    }
    
    def __init__(self, exercise: Exercise):
        """Initialize feedback engine"""
        self.exercise = exercise
        self.validator = ExerciseValidator(exercise)
    
    def generate_feedback(self, validation_result: ValidationResult) -> Dict:
        """Generate feedback based on validation result
        
        Args:
            validation_result: Validation result
            
        Returns:
            Dictionary with prioritized feedback
        """
        feedback_items = []
        
        # Critical feedback (form errors)
        for check in validation_result.failed_checks:
            feedback_items.append({
                'priority': 'critical',
                'message': f"Form issue: {check}",
            })
        
        # Tips for improvement
        if validation_result.score < 1.0:
            feedback_items.extend([
                {
                    'priority': 'tip',
                    'message': tip,
                }
                for tip in self.exercise.tips[:2]  # Top 2 tips
            ])
        
        # Safety warnings
        feedback_items.extend([
            {
                'priority': 'warning',
                'message': warning,
            }
            for warning in self.exercise.warnings
        ])
        
        # Sort by priority
        feedback_items.sort(key=lambda x: self.FEEDBACK_PRIORITY[x['priority']], reverse=True)
        
        return {
            'valid': validation_result.is_valid,
            'score': validation_result.score,
            'feedback': feedback_items[:3],  # Top 3 feedback items
        }
