"""
Model Manager - Quản lý các shared models (MediaPipe, OpenCV, etc.)

Module này quản lý việc khởi tạo và cache các models dùng chung
để tránh load model nhiều lần, tối ưu hiệu năng.
"""
import cv2
import mediapipe as mp
from typing import Optional, Dict, Any
import logging
from ..config import settings

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Singleton class để quản lý các shared models

    Các models được cache trong bộ nhớ để tái sử dụng
    """

    _instance = None
    _models: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._initialize_models()
        return cls._instance

    def _initialize_models(self):
        """
        Khởi tạo các models cơ bản

        INPUT: None
        OUTPUT: None
        SIDE EFFECTS: Load models vào bộ nhớ
        """
        logger.info("Initializing shared models...")

        # Initialize MediaPipe models
        self._models['mp_hands'] = None
        self._models['mp_pose'] = None
        self._models['mp_face'] = None
        self._models['mp_holistic'] = None

        logger.info("Model manager initialized successfully")

    def get_hands_model(self):
        """
        Lấy MediaPipe Hands model

        INPUT: None
        OUTPUT: mediapipe.solutions.hands.Hands object
        USAGE:
            manager = ModelManager()
            hands = manager.get_hands_model()
            results = hands.process(image)
        """
        if self._models['mp_hands'] is None:
            logger.info("Loading MediaPipe Hands model...")
            self._models['mp_hands'] = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=settings.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
            )
        return self._models['mp_hands']

    def get_pose_model(self):
        """
        Lấy MediaPipe Pose model

        INPUT: None
        OUTPUT: mediapipe.solutions.pose.Pose object
        USAGE:
            manager = ModelManager()
            pose = manager.get_pose_model()
            results = pose.process(image)
        """
        if self._models['mp_pose'] is None:
            logger.info("Loading MediaPipe Pose model...")
            self._models['mp_pose'] = mp.solutions.pose.Pose(
                static_image_mode=False,
                min_detection_confidence=settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=settings.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
            )
        return self._models['mp_pose']

    def get_face_model(self):
        """
        Lấy MediaPipe Face Mesh model

        INPUT: None
        OUTPUT: mediapipe.solutions.face_mesh.FaceMesh object
        USAGE:
            manager = ModelManager()
            face = manager.get_face_model()
            results = face.process(image)
        """
        if self._models['mp_face'] is None:
            logger.info("Loading MediaPipe Face Mesh model...")
            self._models['mp_face'] = mp.solutions.face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=settings.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
            )
        return self._models['mp_face']

    def get_holistic_model(self):
        """
        Lấy MediaPipe Holistic model (tích hợp hands, pose, face)

        INPUT: None
        OUTPUT: mediapipe.solutions.holistic.Holistic object
        USAGE:
            manager = ModelManager()
            holistic = manager.get_holistic_model()
            results = holistic.process(image)
        """
        if self._models['mp_holistic'] is None:
            logger.info("Loading MediaPipe Holistic model...")
            self._models['mp_holistic'] = mp.solutions.holistic.Holistic(
                static_image_mode=False,
                min_detection_confidence=settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=settings.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
            )
        return self._models['mp_holistic']

    def extract_hand_landmarks(self, image):
        """
        Trích xuất hand landmarks từ image

        INPUT:
            image: numpy array (BGR format from cv2)
        OUTPUT:
            {
                'success': bool,
                'landmarks': list of hand landmarks hoặc None,
                'handedness': list of handedness ('Left'/'Right') hoặc None
            }
        RAISES:
            Exception nếu có lỗi khi xử lý
        """
        try:
            hands = self.get_hands_model()

            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                landmarks = []
                handedness = []

                for hand_landmarks in results.multi_hand_landmarks:
                    # Convert landmarks to list of dicts
                    landmark_list = []
                    for lm in hand_landmarks.landmark:
                        landmark_list.append({
                            'x': lm.x,
                            'y': lm.y,
                            'z': lm.z,
                            'visibility': getattr(lm, 'visibility', 1.0)
                        })
                    landmarks.append(landmark_list)

                # Get handedness (Left/Right)
                if results.multi_handedness:
                    for hand in results.multi_handedness:
                        handedness.append(hand.classification[0].label)

                return {
                    'success': True,
                    'landmarks': landmarks,
                    'handedness': handedness
                }
            else:
                return {
                    'success': False,
                    'landmarks': None,
                    'handedness': None
                }
        except Exception as e:
            logger.error(f"Error extracting hand landmarks: {str(e)}")
            raise

    def extract_pose_landmarks(self, image):
        """
        Trích xuất pose landmarks từ image

        INPUT:
            image: numpy array (BGR format from cv2)
        OUTPUT:
            {
                'success': bool,
                'landmarks': list of pose landmarks hoặc None
            }
        RAISES:
            Exception nếu có lỗi khi xử lý
        """
        try:
            pose = self.get_pose_model()

            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = []
                for lm in results.pose_landmarks.landmark:
                    landmarks.append({
                        'x': lm.x,
                        'y': lm.y,
                        'z': lm.z,
                        'visibility': lm.visibility
                    })

                return {
                    'success': True,
                    'landmarks': landmarks
                }
            else:
                return {
                    'success': False,
                    'landmarks': None
                }
        except Exception as e:
            logger.error(f"Error extracting pose landmarks: {str(e)}")
            raise

    def extract_holistic_landmarks(self, image):
        """
        Trích xuất tất cả landmarks (hands, pose, face) từ image

        INPUT:
            image: numpy array (BGR format from cv2)
        OUTPUT:
            {
                'success': bool,
                'face_landmarks': list hoặc None,
                'pose_landmarks': list hoặc None,
                'left_hand_landmarks': list hoặc None,
                'right_hand_landmarks': list hoặc None
            }
        RAISES:
            Exception nếu có lỗi khi xử lý
        """
        try:
            holistic = self.get_holistic_model()

            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process
            results = holistic.process(image_rgb)

            def landmarks_to_list(landmarks):
                if landmarks is None:
                    return None
                return [{
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z,
                    'visibility': getattr(lm, 'visibility', 1.0)
                } for lm in landmarks.landmark]

            return {
                'success': True,
                'face_landmarks': landmarks_to_list(results.face_landmarks),
                'pose_landmarks': landmarks_to_list(results.pose_landmarks),
                'left_hand_landmarks': landmarks_to_list(results.left_hand_landmarks),
                'right_hand_landmarks': landmarks_to_list(results.right_hand_landmarks)
            }
        except Exception as e:
            logger.error(f"Error extracting holistic landmarks: {str(e)}")
            raise

    def release_models(self):
        """
        Giải phóng tất cả models khỏi bộ nhớ

        INPUT: None
        OUTPUT: None
        SIDE EFFECTS: Release models từ memory
        """
        for key in self._models:
            if self._models[key] is not None:
                if hasattr(self._models[key], 'close'):
                    self._models[key].close()
                self._models[key] = None
        logger.info("All models released")


# Global instance
model_manager = ModelManager()
