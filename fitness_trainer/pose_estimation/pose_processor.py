"""Pose processing utilities"""
import numpy as np
from typing import List, Tuple, Dict, Optional
from .pose_detector import LandmarkPoint, PoseDetector


class PoseProcessor:
    """Utility class for processing pose data"""
    
    @staticmethod
    def get_distance(point1: LandmarkPoint, point2: LandmarkPoint) -> float:
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    @staticmethod
    def get_distance_3d(point1: LandmarkPoint, point2: LandmarkPoint) -> float:
        """Calculate 3D Euclidean distance between two points"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)
    
    @staticmethod
    def normalize_landmarks(landmarks: Dict[str, LandmarkPoint], 
                           reference_point: LandmarkPoint) -> Dict[str, LandmarkPoint]:
        """Normalize landmarks relative to a reference point (e.g., neck)
        
        Args:
            landmarks: Dictionary of landmarks
            reference_point: Reference point for normalization
            
        Returns:
            Dictionary of normalized landmarks
        """
        normalized = {}
        for name, point in landmarks.items():
            normalized[name] = LandmarkPoint(
                x=point.x - reference_point.x,
                y=point.y - reference_point.y,
                z=point.z - reference_point.z,
                visibility=point.visibility
            )
        return normalized
    
    @staticmethod
    def is_hand_raised(detector: PoseDetector, hand: str = 'left') -> bool:
        """Check if hand is raised above shoulder
        
        Args:
            detector: PoseDetector instance
            hand: 'left' or 'right'
            
        Returns:
            True if hand is raised above shoulder
        """
        if hand == 'left':
            hand_landmark = detector.get_landmark('LEFT_WRIST')
            shoulder_landmark = detector.get_landmark('LEFT_SHOULDER')
        else:
            hand_landmark = detector.get_landmark('RIGHT_WRIST')
            shoulder_landmark = detector.get_landmark('RIGHT_SHOULDER')
        
        if not (hand_landmark and shoulder_landmark):
            return False
        
        return hand_landmark.y < shoulder_landmark.y
    
    @staticmethod
    def is_standing(detector: PoseDetector) -> bool:
        """Check if person is standing (both feet visible, knees visible)"""
        left_ankle = detector.get_landmark('LEFT_ANKLE')
        right_ankle = detector.get_landmark('RIGHT_ANKLE')
        left_knee = detector.get_landmark('LEFT_KNEE')
        right_knee = detector.get_landmark('RIGHT_KNEE')
        
        if not all([left_ankle, right_ankle, left_knee, right_knee]):
            return False
        
        # Standing if all joints are visible
        return all(p.visibility > 0.5 for p in [left_ankle, right_ankle, left_knee, right_knee])
    
    @staticmethod
    def posture_analysis(detector: PoseDetector) -> Dict[str, bool]:
        """Analyze current posture
        
        Returns:
            Dictionary with posture analysis results
        """
        analysis = {}
        
        # Check alignment (head over shoulders over hips)
        head = detector.get_landmark('NOSE')
        left_shoulder = detector.get_landmark('LEFT_SHOULDER')
        right_shoulder = detector.get_landmark('RIGHT_SHOULDER')
        left_hip = detector.get_landmark('LEFT_HIP')
        right_hip = detector.get_landmark('RIGHT_HIP')
        
        if all([head, left_shoulder, right_shoulder, left_hip, right_hip]):
            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            hip_center_x = (left_hip.x + right_hip.x) / 2
            
            # Check if alignment is good (within 5% tolerance)
            alignment_tolerance = 0.05
            frame_width = detector.frame_width if hasattr(detector, 'frame_width') else 640
            frame_height = detector.frame_height if hasattr(detector, 'frame_height') else 480
            
            analysis['good_alignment'] = abs(head.x - shoulder_center_x) / frame_width < alignment_tolerance
            analysis['shoulders_level'] = abs(left_shoulder.y - right_shoulder.y) / frame_height < 0.05
            analysis['hips_level'] = abs(left_hip.y - right_hip.y) / frame_height < 0.05
        
        return analysis
    
    @staticmethod
    def get_body_center(detector: PoseDetector) -> Tuple[float, float]:
        """Get approximate center of body (midpoint of shoulders and hips)"""
        left_hip = detector.get_landmark('LEFT_HIP')
        right_hip = detector.get_landmark('RIGHT_HIP')
        left_shoulder = detector.get_landmark('LEFT_SHOULDER')
        right_shoulder = detector.get_landmark('RIGHT_SHOULDER')
        
        if all([left_hip, right_hip, left_shoulder, right_shoulder]):
            center_x = (left_hip.x + right_hip.x + left_shoulder.x + right_shoulder.x) / 4
            center_y = (left_hip.y + right_hip.y + left_shoulder.y + right_shoulder.y) / 4
            return (center_x, center_y)
        
        return (0, 0)


class JointAnalyzer:
    """Analyze joint movements and angles"""
    
    # Typical angle ranges for various exercise positions
    ANGLE_RANGES = {
        'arm': {
            'fully_extended': (170, 180),
            'bent': (90, 110),
            'flexed': (0, 30),
        },
        'leg': {
            'fully_extended': (170, 180),
            'bent': (80, 120),
            'flexed': (0, 30),
        },
        'back': {
            'straight': (170, 180),
            'slightly_bent': (150, 170),
            'bent': (90, 150),
        }
    }
    
    @staticmethod
    def analyze_arm_curl(detector: PoseDetector, arm: str = 'left') -> Dict:
        """Analyze bicep curl form
        
        Args:
            detector: PoseDetector instance
            arm: 'left' or 'right'
            
        Returns:
            Dictionary with form analysis
        """
        if arm == 'left':
            shoulder = detector.get_landmark('LEFT_SHOULDER')
            elbow = detector.get_landmark('LEFT_ELBOW')
            wrist = detector.get_landmark('LEFT_WRIST')
        else:
            shoulder = detector.get_landmark('RIGHT_SHOULDER')
            elbow = detector.get_landmark('RIGHT_ELBOW')
            wrist = detector.get_landmark('RIGHT_WRIST')
        
        if not all([shoulder, elbow, wrist]):
            return {'error': 'Landmarks not detected'}
        
        angle = JointAnalyzer._calculate_angle(shoulder, elbow, wrist)
        
        analysis = {
            'elbow_angle': angle,
            'position': 'starting' if angle > 150 else 'lifted' if angle < 90 else 'mid-range',
            'form_check': {
                'stable_shoulder': abs(shoulder.y - 0) < 50,  # Shoulder not raising
                'elbow_movement': True,
            }
        }
        
        return analysis
    
    @staticmethod
    def analyze_squat(detector: PoseDetector) -> Dict:
        """Analyze squat form
        
        Returns:
            Dictionary with squat form analysis
        """
        left_hip = detector.get_landmark('LEFT_HIP')
        right_hip = detector.get_landmark('RIGHT_HIP')
        left_knee = detector.get_landmark('LEFT_KNEE')
        right_knee = detector.get_landmark('RIGHT_KNEE')
        left_ankle = detector.get_landmark('LEFT_ANKLE')
        right_ankle = detector.get_landmark('RIGHT_ANKLE')
        
        if not all([left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]):
            return {'error': 'Landmarks not detected'}
        
        left_knee_angle = JointAnalyzer._calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = JointAnalyzer._calculate_angle(right_hip, right_knee, right_ankle)
        
        # Check knee alignment with ankles
        frame_width = 640  # Default value; should be updated if PoseDetector is passed
        left_knee_aligned = abs(left_knee.x - left_ankle.x) / frame_width < 0.1
        right_knee_aligned = abs(right_knee.x - right_ankle.x) / frame_width < 0.1
        
        analysis = {
            'left_knee_angle': left_knee_angle,
            'right_knee_angle': right_knee_angle,
            'depth': 'shallow' if min(left_knee_angle, right_knee_angle) > 120 else 'parallel' if min(left_knee_angle, right_knee_angle) > 80 else 'deep',
            'form_check': {
                'knees_tracking': left_knee_aligned and right_knee_aligned,
                'balanced': abs(left_knee_angle - right_knee_angle) < 15,
                'depth_sufficient': min(left_knee_angle, right_knee_angle) < 120,
            }
        }
        
        return analysis
    
    @staticmethod
    def _calculate_angle(p1: LandmarkPoint, p2: LandmarkPoint, p3: LandmarkPoint) -> float:
        """Calculate angle at p2 using three points"""
        v1 = np.array([p1.x - p2.x, p1.y - p2.y])
        v2 = np.array([p3.x - p2.x, p3.y - p2.y])
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    @staticmethod
    def check_angle_in_range(angle: float, min_angle: float, max_angle: float) -> bool:
        """Check if angle is within expected range"""
        return min_angle <= angle <= max_angle
