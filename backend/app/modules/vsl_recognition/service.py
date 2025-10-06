"""
VSL Recognition Service - Group 1
Business logic cho VSL recognition

STUDENT TODO: Implement các functions dưới đây
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import time
import base64
import numpy as np
import cv2

from ...core.model_manager import model_manager

logger = logging.getLogger(__name__)


def recognize_from_video(video_path: str, options: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Nhận diện VSL từ video file

    INPUT:
        video_path: str - Đường dẫn đến video file
        options: dict - Các tùy chọn:
            - sample_rate: int - Lấy 1 frame mỗi N frames (default: 5)
            - confidence_threshold: float - Ngưỡng confidence (default: 0.5)
            - max_frames: int - Số frames tối đa xử lý (default: None)

    OUTPUT:
        {
            'success': bool,
            'detected_text': str - Text được nhận diện,
            'confidence': float - Độ tin cậy (0-1),
            'frame_count': int - Số frames đã xử lý,
            'landmarks_sequence': list - Sequence of landmarks (optional),
            'processing_time': float - Thời gian xử lý (seconds),
            'error': str or None
        }

    STUDENT TODO:
        1. Load video và extract frames (sử dụng core/utils.py::extract_frames_from_video)
        2. Với mỗi frame, extract landmarks (sử dụng core/model_manager.py::extract_holistic_landmarks)
        3. Xây dựng sequence of landmarks
        4. Load trained model và predict từ sequence
        5. Post-process kết quả
        6. Return kết quả theo format trên

    EXAMPLE:
        result = recognize_from_video('/path/to/video.mp4')
        print(result['detected_text'])  # "Xin chào"
    """
    # PLACEHOLDER - Students implement this
    print("[VSL_RECOGNITION] recognize_from_video called")
    print(f"  - video_path: {video_path}")
    print(f"  - options: {options}")

    # TODO: Implement actual recognition logic
    return {
        'success': True,
        'detected_text': "PLACEHOLDER - Implement recognition logic",
        'confidence': 0.0,
        'frame_count': 0,
        'landmarks_sequence': [],
        'processing_time': 0.0,
        'error': None
    }


def recognize_from_image(image_path: str, options: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Nhận diện VSL từ hình ảnh (single frame)

    INPUT:
        image_path: str - Đường dẫn đến image file
        options: dict - Các tùy chọn:
            - confidence_threshold: float - Ngưỡng confidence (default: 0.5)

    OUTPUT:
        {
            'success': bool,
            'detected_gesture': str - Gesture được nhận diện,
            'confidence': float - Độ tin cậy (0-1),
            'landmarks': dict - Landmarks data,
            'processing_time': float,
            'error': str or None
        }

    STUDENT TODO:
        1. Load image (sử dụng core/utils.py::load_image)
        2. Extract landmarks (sử dụng core/model_manager.py::extract_holistic_landmarks)
        3. Load trained model và predict gesture từ landmarks
        4. Return kết quả

    EXAMPLE:
        result = recognize_from_image('/path/to/image.jpg')
        print(result['detected_gesture'])  # "Chào"
    """
    # PLACEHOLDER
    print("[VSL_RECOGNITION] recognize_from_image called")
    print(f"  - image_path: {image_path}")
    print(f"  - options: {options}")

    # TODO: Implement actual recognition logic
    return {
        'success': True,
        'detected_gesture': "PLACEHOLDER - Implement recognition logic",
        'confidence': 0.0,
        'landmarks': {},
        'processing_time': 0.0,
        'error': None
    }


def recognize_realtime_frame(frame_data: bytes, options: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Nhận diện VSL từ single frame (realtime camera)

    INPUT:
        frame_data: bytes - Binary data của frame (BGR image)
        options: dict - Các tùy chọn

    OUTPUT:
        {
            'success': bool,
            'detected_gesture': str or None,
            'confidence': float,
            'landmarks': dict,
            'processing_time': float,
            'error': str or None
        }

    STUDENT TODO:
        1. Convert frame_data to numpy array
        2. Extract landmarks (sử dụng core/model_manager.py)
        3. Predict gesture từ landmarks
        4. Return kết quả nhanh (< 100ms để realtime)

    NOTE: Function này phải tối ưu cho tốc độ vì được gọi liên tục từ webcam
    """
    # PLACEHOLDER
    print("[VSL_RECOGNITION] recognize_realtime_frame called")

    # TODO: Implement realtime recognition
    return {
        'success': True,
        'detected_gesture': None,
        'confidence': 0.0,
        'landmarks': {},
        'processing_time': 0.0,
        'error': None
    }


def detect_gesture(landmarks: Dict, gesture_templates: list) -> Dict[str, Any]:
    """
    So sánh landmarks với gesture templates để detect gesture

    INPUT:
        landmarks: dict - Landmarks data từ MediaPipe
            {
                'left_hand_landmarks': [...],
                'right_hand_landmarks': [...],
                'pose_landmarks': [...]
            }
        gesture_templates: list - Danh sách gesture templates từ database

    OUTPUT:
        {
            'success': bool,
            'gesture_name': str or None,
            'confidence': float,
            'matched_template_id': int or None
        }

    STUDENT TODO:
        1. Normalize landmarks
        2. So sánh với từng template (tính similarity)
        3. Chọn template có similarity cao nhất
        4. Return kết quả

    ALGORITHM SUGGESTION:
        - Dynamic Time Warping (DTW) cho sequence matching
        - Cosine similarity cho single frame
        - Template matching với threshold
    """
    # PLACEHOLDER
    print("[VSL_RECOGNITION] detect_gesture called")
    print(f"  - landmarks keys: {landmarks.keys() if landmarks else None}")
    print(f"  - template count: {len(gesture_templates)}")

    # TODO: Implement gesture detection
    return {
        'success': True,
        'gesture_name': None,
        'confidence': 0.0,
        'matched_template_id': None
    }


def detect_emotion(face_landmarks: list) -> Dict[str, Any]:
    """
    Nhận diện cảm xúc từ face landmarks

    INPUT:
        face_landmarks: list - Face landmarks từ MediaPipe
            [
                {'x': 0.5, 'y': 0.3, 'z': 0.1},
                ...
            ]

    OUTPUT:
        {
            'success': bool,
            'emotion': str - 'happy', 'sad', 'angry', 'neutral', etc.,
            'confidence': float
        }

    STUDENT TODO:
        1. Extract features từ face landmarks (mouth, eyebrows, eyes)
        2. Load trained emotion model
        3. Predict emotion
        4. Return kết quả

    EMOTIONS TO DETECT:
        - neutral, happy, sad, angry, surprised, confused
    """
    # PLACEHOLDER
    print("[VSL_RECOGNITION] detect_emotion called")
    print(f"  - face_landmarks count: {len(face_landmarks) if face_landmarks else 0}")

    # TODO: Implement emotion detection
    return {
        'success': True,
        'emotion': 'neutral',
        'confidence': 0.0
    }


def process_video_hand_keypoints(
    video_path: str,
    sample_rate: int = 5,
    max_frames: Optional[int] = None
) -> Dict[str, Any]:
    """
    Process video file and extract hand keypoints from each frame

    This function processes a video file frame by frame, detecting hand keypoints
    using MediaPipe Hands. Useful for analyzing gesture sequences in videos.

    INPUT:
        video_path: str - Path to video file
        sample_rate: int - Process 1 frame every N frames (default: 5)
            Example: sample_rate=5 means process frames 0, 5, 10, 15...
        max_frames: int or None - Maximum frames to process (default: None = all)

    OUTPUT:
        {
            'success': bool - True if processing succeeded,
            'total_frames_processed': int - Number of frames analyzed,
            'hands_detected_frames': int - Frames where hands were detected,
            'detection_rate': float - Percentage of frames with hands detected,
            'sample_frames': list - Sample frames with keypoint data (max 10):
                [
                    {
                        'frame_number': int,
                        'timestamp': float,
                        'hands_detected': int,
                        'hands': [
                            {
                                'hand_type': str,
                                'keypoints': [...]
                            }
                        ]
                    }
                ],
            'summary': dict - Summary statistics:
                {
                    'left_hand_frames': int,
                    'right_hand_frames': int,
                    'both_hands_frames': int,
                    'avg_hands_per_frame': float
                },
            'error': str or None
        }

    USAGE:
        result = process_video_hand_keypoints('path/to/video.mp4', sample_rate=10)
        print(f"Processed {result['total_frames_processed']} frames")
        print(f"Hands detected in {result['hands_detected_frames']} frames")

    NOTE:
        - For long videos, use higher sample_rate to reduce processing time
        - Set max_frames to limit processing for testing
        - Each frame shows up to 2 hands (left/right)
        - Sample frames limited to 10 to keep response size manageable

    STUDENT TODO:
        Students can enhance this to:
        1. Add gesture sequence detection across frames
        2. Generate gesture timeline/heatmap
        3. Export keypoints to CSV/JSON for training
        4. Add gesture classification per frame
    """
    start_time = time.time()

    try:
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

        # Get video properties
        total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        logger.info(f"Processing video: {video_path}")
        logger.info(f"  Total frames: {total_video_frames}, FPS: {fps}")
        logger.info(f"  Sample rate: {sample_rate}, Max frames: {max_frames}")

        # Initialize counters
        frame_count = 0
        processed_count = 0
        hands_detected_count = 0
        left_hand_count = 0
        right_hand_count = 0
        both_hands_count = 0
        sample_frames = []

        # Process frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Check max frames limit
            if max_frames and processed_count >= max_frames:
                break

            # Process only sampled frames
            if frame_count % sample_rate == 0:
                # Extract hand landmarks
                landmarks_result = model_manager.extract_hand_landmarks(frame)

                frame_data = {
                    'frame_number': frame_count,
                    'timestamp': round(frame_count / fps, 2) if fps > 0 else 0,
                    'hands_detected': 0,
                    'hands': []
                }

                if landmarks_result['success'] and landmarks_result['landmarks']:
                    hands_detected = len(landmarks_result['landmarks'])
                    frame_data['hands_detected'] = hands_detected
                    hands_detected_count += 1

                    # Count hand types
                    has_left = False
                    has_right = False

                    # Process each detected hand
                    for i, hand_landmarks in enumerate(landmarks_result['landmarks']):
                        hand_type = 'Unknown'
                        if landmarks_result['handedness'] and i < len(landmarks_result['handedness']):
                            hand_type = landmarks_result['handedness'][i]
                            if hand_type == 'Left':
                                has_left = True
                            elif hand_type == 'Right':
                                has_right = True

                        # Format keypoints (only first 5 for sample to reduce size)
                        keypoints = []
                        for idx, landmark in enumerate(hand_landmarks[:5]):
                            keypoints.append({
                                'id': idx,
                                'x': round(landmark['x'], 4),
                                'y': round(landmark['y'], 4),
                                'z': round(landmark['z'], 4)
                            })

                        frame_data['hands'].append({
                            'hand_type': hand_type,
                            'keypoints': keypoints,
                            'total_keypoints': len(hand_landmarks)
                        })

                    # Update hand type counters
                    if has_left and has_right:
                        both_hands_count += 1
                    elif has_left:
                        left_hand_count += 1
                    elif has_right:
                        right_hand_count += 1

                # Save sample frames (max 10 evenly distributed)
                if len(sample_frames) < 10 or processed_count % (max(1, (max_frames or total_video_frames) // 10)) == 0:
                    if len(sample_frames) < 10:
                        sample_frames.append(frame_data)

                processed_count += 1

                # Log progress every 50 frames
                if processed_count % 50 == 0:
                    logger.info(f"  Processed {processed_count} frames...")

            frame_count += 1

        cap.release()

        processing_time = time.time() - start_time

        # Calculate statistics
        detection_rate = (hands_detected_count / processed_count * 100) if processed_count > 0 else 0
        avg_hands = (left_hand_count + right_hand_count + 2 * both_hands_count) / processed_count if processed_count > 0 else 0

        result = {
            'success': True,
            'total_frames_processed': processed_count,
            'hands_detected_frames': hands_detected_count,
            'detection_rate': round(detection_rate, 2),
            'sample_frames': sample_frames,
            'summary': {
                'left_hand_frames': left_hand_count,
                'right_hand_frames': right_hand_count,
                'both_hands_frames': both_hands_count,
                'avg_hands_per_frame': round(avg_hands, 2),
                'video_fps': round(fps, 2),
                'video_duration_seconds': round(total_video_frames / fps, 2) if fps > 0 else 0
            },
            'processing_time': round(processing_time, 2),
            'error': None
        }

        logger.info(f"Video processing complete:")
        logger.info(f"  Processed: {processed_count} frames")
        logger.info(f"  Hands detected: {hands_detected_count} frames ({detection_rate:.1f}%)")
        logger.info(f"  Processing time: {processing_time:.2f}s")

        return result

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        return {
            'success': False,
            'total_frames_processed': 0,
            'hands_detected_frames': 0,
            'detection_rate': 0,
            'sample_frames': [],
            'summary': {},
            'processing_time': 0,
            'error': str(e)
        }


def detect_hand_keypoints_realtime(frame_base64: str) -> Dict[str, Any]:
    """
    Detect hand keypoints from a single frame in real-time

    This function is designed for real-time hand tracking via WebSocket.
    It processes a base64-encoded frame and returns hand keypoint locations.

    INPUT:
        frame_base64: str - Base64-encoded JPEG/PNG image from webcam
            Example: "data:image/jpeg;base64,/9j/4AAQSkZJRg..." or just the base64 string

    OUTPUT:
        {
            'success': bool - True if processing succeeded,
            'hands_detected': int - Number of hands detected (0-2),
            'hands': list - List of detected hands:
                [
                    {
                        'hand_type': str - 'Left' or 'Right',
                        'keypoints': list - 21 hand landmarks:
                            [
                                {'id': 0, 'x': float, 'y': float, 'z': float},
                                {'id': 1, 'x': float, 'y': float, 'z': float},
                                ...  # 21 keypoints total
                            ]
                    }
                ],
            'timestamp': float - Processing timestamp,
            'processing_time': float - Time taken to process (seconds),
            'error': str or None - Error message if failed
        }

    USAGE:
        # Called from WebSocket endpoint
        result = detect_hand_keypoints_realtime(base64_frame)
        if result['success']:
            print(f"Detected {result['hands_detected']} hands")
            for hand in result['hands']:
                print(f"{hand['hand_type']} hand: {len(hand['keypoints'])} keypoints")

    NOTE:
        - MediaPipe Hands detects 21 keypoints per hand
        - Coordinates are normalized (0.0 to 1.0)
        - x, y are in image coordinates, z is depth
        - Optimized for real-time performance (< 100ms per frame)

    HAND KEYPOINT IDS:
        0: WRIST
        1-4: THUMB (CMC, MCP, IP, TIP)
        5-8: INDEX (MCP, PIP, DIP, TIP)
        9-12: MIDDLE (MCP, PIP, DIP, TIP)
        13-16: RING (MCP, PIP, DIP, TIP)
        17-20: PINKY (MCP, PIP, DIP, TIP)
    """
    start_time = time.time()

    try:
        # Step 1: Decode base64 image
        # Handle data URL format (data:image/jpeg;base64,xxxxx)
        if ',' in frame_base64:
            frame_base64 = frame_base64.split(',')[1]

        # Decode base64 to bytes
        image_bytes = base64.b64decode(frame_base64)

        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Failed to decode image from base64")

        # Step 2: Extract hand landmarks using ModelManager
        landmarks_result = model_manager.extract_hand_landmarks(image)

        # Step 3: Format results
        hands = []
        hands_detected = 0

        if landmarks_result['success'] and landmarks_result['landmarks']:
            hands_detected = len(landmarks_result['landmarks'])

            # Process each detected hand
            for i, hand_landmarks in enumerate(landmarks_result['landmarks']):
                # Get hand type (Left/Right)
                hand_type = 'Unknown'
                if landmarks_result['handedness'] and i < len(landmarks_result['handedness']):
                    hand_type = landmarks_result['handedness'][i]

                # Format keypoints
                keypoints = []
                for idx, landmark in enumerate(hand_landmarks):
                    keypoints.append({
                        'id': idx,
                        'x': round(landmark['x'], 4),
                        'y': round(landmark['y'], 4),
                        'z': round(landmark['z'], 4)
                    })

                hands.append({
                    'hand_type': hand_type,
                    'keypoints': keypoints
                })

        processing_time = time.time() - start_time

        return {
            'success': True,
            'hands_detected': hands_detected,
            'hands': hands,
            'timestamp': time.time(),
            'processing_time': round(processing_time, 4),
            'error': None
        }

    except base64.binascii.Error as e:
        logger.error(f"Base64 decode error: {str(e)}")
        return {
            'success': False,
            'hands_detected': 0,
            'hands': [],
            'timestamp': time.time(),
            'processing_time': 0.0,
            'error': f"Invalid base64 image: {str(e)}"
        }

    except Exception as e:
        logger.error(f"Error in hand keypoint detection: {str(e)}", exc_info=True)
        return {
            'success': False,
            'hands_detected': 0,
            'hands': [],
            'timestamp': time.time(),
            'processing_time': 0.0,
            'error': str(e)
        }
