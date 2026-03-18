"""Pose Detection Module using MediaPipe"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class LandmarkPoint:
    """Represents a single pose landmark"""
    x: float
    y: float
    z: float
    visibility: float
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convert to tuple format"""
        return (self.x, self.y, self.z, self.visibility)
    
    def to_2d(self) -> Tuple[float, float]:
        """Get 2D coordinates (x, y)"""
        return (self.x, self.y)


class PoseDetector:
    """Real-time pose detection using MediaPipe"""
    
    # Landmark indices for major body parts
    LANDMARKS = {
        'NOSE': 0,
        'LEFT_EYE_INNER': 1,
        'LEFT_EYE': 2,
        'LEFT_EYE_OUTER': 3,
        'RIGHT_EYE_INNER': 4,
        'RIGHT_EYE': 5,
        'RIGHT_EYE_OUTER': 6,
        'LEFT_EAR': 7,
        'RIGHT_EAR': 8,
        'MOUTH_LEFT': 9,
        'MOUTH_RIGHT': 10,
        'LEFT_SHOULDER': 11,
        'RIGHT_SHOULDER': 12,
        'LEFT_ELBOW': 13,
        'RIGHT_ELBOW': 14,
        'LEFT_WRIST': 15,
        'RIGHT_WRIST': 16,
        'LEFT_PINKY': 17,
        'RIGHT_PINKY': 18,
        'LEFT_INDEX': 19,
        'RIGHT_INDEX': 20,
        'LEFT_THUMB': 21,
        'RIGHT_THUMB': 22,
        'LEFT_HIP': 23,
        'RIGHT_HIP': 24,
        'LEFT_KNEE': 25,
        'RIGHT_KNEE': 26,
        'LEFT_ANKLE': 27,
        'RIGHT_ANKLE': 28,
        'LEFT_HEEL': 29,
        'RIGHT_HEEL': 30,
        'LEFT_FOOT_INDEX': 31,
        'RIGHT_FOOT_INDEX': 32,
    }
    
    # Key joints for exercise analysis
    KEY_JOINTS = {
        'left_arm': ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'],
        'right_arm': ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST'],
        'left_leg': ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'],
        'right_leg': ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'],
        'torso': ['LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_HIP', 'RIGHT_HIP'],
    }
    
    def __init__(self, min_detection_confidence: float = 0.5, 
                 min_tracking_confidence: float = 0.5):
        """Initialize the pose detector
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.frame_width = 640
        self.frame_height = 480
        self.landmarks = {}
        
    def detect(self, frame: np.ndarray) -> bool:
        """Detect pose in the given frame
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            True if pose detected, False otherwise
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            self._process_landmarks(results.pose_landmarks, frame.shape)
            return True
        
        self.landmarks = {}
        return False
    
    def _process_landmarks(self, pose_landmarks, frame_shape):
        """Process detected landmarks"""
        height, width = frame_shape[:2]
        self.frame_height = height
        self.frame_width = width
        
        self.landmarks = {}
        for name, idx in self.LANDMARKS.items():
            landmark = pose_landmarks.landmark[idx]
            self.landmarks[name] = LandmarkPoint(
                x=landmark.x * width,
                y=landmark.y * height,
                z=landmark.z * width,
                visibility=landmark.visibility
            )
    
    def get_landmark(self, name: str) -> Optional[LandmarkPoint]:
        """Get a specific landmark by name
        
        Args:
            name: Landmark name (e.g., 'LEFT_SHOULDER')
            
        Returns:
            LandmarkPoint or None if not detected
        """
        return self.landmarks.get(name)
    
    def get_all_landmarks(self) -> dict:
        """Get all detected landmarks"""
        return self.landmarks.copy()
    
    def draw_pose(self, frame: np.ndarray, thickness: int = 2, 
                  circle_radius: int = 3) -> np.ndarray:
        """Draw pose landmarks and connections on frame
        
        Args:
            frame: Input frame
            thickness: Line thickness
            circle_radius: Circle radius for joints
            
        Returns:
            Frame with drawn pose
        """
        output_frame = frame.copy()
        
        if not self.landmarks:
            return output_frame
        
        # Draw circles at landmark positions
        for name, point in self.landmarks.items():
            if point.visibility > 0.5:
                x, y = int(point.x), int(point.y)
                cv2.circle(output_frame, (x, y), circle_radius, (0, 255, 0), -1)
        
        # Draw connections between joints
        connections = [
            ('LEFT_SHOULDER', 'LEFT_ELBOW'),
            ('LEFT_ELBOW', 'LEFT_WRIST'),
            ('RIGHT_SHOULDER', 'RIGHT_ELBOW'),
            ('RIGHT_ELBOW', 'RIGHT_WRIST'),
            ('LEFT_HIP', 'LEFT_KNEE'),
            ('LEFT_KNEE', 'LEFT_ANKLE'),
            ('RIGHT_HIP', 'RIGHT_KNEE'),
            ('RIGHT_KNEE', 'RIGHT_ANKLE'),
            ('LEFT_SHOULDER', 'RIGHT_SHOULDER'),
            ('LEFT_SHOULDER', 'LEFT_HIP'),
            ('RIGHT_SHOULDER', 'RIGHT_HIP'),
            ('LEFT_HIP', 'RIGHT_HIP'),
        ]
        
        for start, end in connections:
            start_point = self.landmarks.get(start)
            end_point = self.landmarks.get(end)
            
            if start_point and end_point and start_point.visibility > 0.5 and end_point.visibility > 0.5:
                x1, y1 = int(start_point.x), int(start_point.y)
                x2, y2 = int(end_point.x), int(end_point.y)
                cv2.line(output_frame, (x1, y1), (x2, y2), (0, 255, 0), thickness)
        
        return output_frame
    
    def get_joint_angle(self, joint_start: str, joint_center: str, 
                        joint_end: str) -> Optional[float]:
        """Calculate angle at a joint using three landmarks
        
        Args:
            joint_start: Starting joint name
            joint_center: Center/middle joint name
            joint_end: Ending joint name
            
        Returns:
            Angle in degrees or None if landmarks not detected
        """
        p1 = self.get_landmark(joint_start)
        p2 = self.get_landmark(joint_center)
        p3 = self.get_landmark(joint_end)
        
        if not (p1 and p2 and p3):
            return None
        
        # Vector from p2 to p1
        v1 = np.array([p1.x - p2.x, p1.y - p2.y])
        # Vector from p2 to p3
        v2 = np.array([p3.x - p2.x, p3.y - p2.y])
        
        # Calculate angle
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        angle_degrees = np.degrees(angle)
        
        return angle_degrees
    
    def is_pose_detected(self) -> bool:
        """Check if pose was detected in current frame"""
        return len(self.landmarks) > 0
    
    def release(self):
        """Release resources"""
        if self.pose:
            self.pose.close()
