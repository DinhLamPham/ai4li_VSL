"""
VSL Recognition Router - API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import time
import logging
from pathlib import Path

from ...database.db import get_db
from ...database.schemas import VSLRecognitionResponse, APIResponse
from ...config import settings
from ...core.utils import save_uploaded_file, validate_file_extension, create_response
from . import service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vsl", tags=["VSL Recognition"])


@router.post("/recognize-video", response_model=APIResponse)
async def recognize_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Nhận diện VSL từ video file

    **INPUT:**
    - file: Video file (mp4, avi, mov, mkv)

    **OUTPUT:**
    - success: bool
    - data: VSL recognition results
    - message: Status message

    **STUDENT TODO:**
    - Validate file
    - Save file
    - Call service.recognize_from_video()
    - Return results
    """
    try:
        start_time = time.time()

        # Validate extension
        if not validate_file_extension(file.filename, settings.ALLOWED_VIDEO_EXTENSIONS):
            return create_response(
                success=False,
                message="Invalid file extension. Allowed: mp4, avi, mov, mkv",
                error="Invalid file type"
            )

        # Save uploaded file
        file_content = await file.read()
        file_path = save_uploaded_file(
            file_content,
            file.filename,
            settings.RAW_DATA_DIR / "videos"
        )

        # Call recognition service
        result = service.recognize_from_video(file_path)

        processing_time = time.time() - start_time
        result['processing_time'] = processing_time

        return create_response(
            success=result['success'],
            message="Video processed successfully" if result['success'] else "Processing failed",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Error processing video",
            error=str(e)
        )


@router.post("/recognize-image", response_model=APIResponse)
async def recognize_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Nhận diện VSL từ image file

    **INPUT:**
    - file: Image file (jpg, jpeg, png, bmp)

    **OUTPUT:**
    - success: bool
    - data: Recognition results

    **STUDENT TODO:**
    - Validate file
    - Save file
    - Call service.recognize_from_image()
    - Return results
    """
    try:
        # Validate extension
        if not validate_file_extension(file.filename, settings.ALLOWED_IMAGE_EXTENSIONS):
            return create_response(
                success=False,
                message="Invalid file extension. Allowed: jpg, jpeg, png, bmp",
                error="Invalid file type"
            )

        # Save uploaded file
        file_content = await file.read()
        file_path = save_uploaded_file(
            file_content,
            file.filename,
            settings.RAW_DATA_DIR / "images"
        )

        # Call recognition service
        result = service.recognize_from_image(file_path)

        return create_response(
            success=result['success'],
            message="Image processed successfully" if result['success'] else "Processing failed",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Error processing image",
            error=str(e)
        )


@router.get("/gestures", response_model=APIResponse)
async def list_gestures(db: Session = Depends(get_db)):
    """
    Liệt kê tất cả gestures có trong database

    **OUTPUT:**
    - List of gesture templates

    **STUDENT TODO:**
    - Query database cho gesture_templates
    - Return list
    """
    # PLACEHOLDER
    print("[API] GET /vsl/gestures called")

    # TODO: Query database
    return create_response(
        success=True,
        message="Gestures retrieved",
        data={"gestures": []}
    )


@router.post("/gesture/detect", response_model=APIResponse)
async def detect_gesture_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Detect specific gesture từ image/video

    **INPUT:**
    - file: Image or video file

    **OUTPUT:**
    - Detected gesture name and confidence

    **STUDENT TODO:**
    - Extract landmarks từ file
    - Load gesture templates từ DB
    - Call service.detect_gesture()
    - Return results
    """
    # PLACEHOLDER
    print("[API] POST /vsl/gesture/detect called")

    # TODO: Implement gesture detection
    return create_response(
        success=True,
        message="PLACEHOLDER - Implement gesture detection",
        data={}
    )


@router.post("/emotion/detect", response_model=APIResponse)
async def detect_emotion_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Detect emotion từ image

    **INPUT:**
    - file: Image file (containing face)

    **OUTPUT:**
    - Detected emotion and confidence

    **STUDENT TODO:**
    - Load image
    - Extract face landmarks
    - Call service.detect_emotion()
    - Return results
    """
    # PLACEHOLDER
    print("[API] POST /vsl/emotion/detect called")

    # TODO: Implement emotion detection
    return create_response(
        success=True,
        message="PLACEHOLDER - Implement emotion detection",
        data={}
    )


@router.post("/hand-tracking/video", response_model=APIResponse)
async def hand_tracking_video(
    file: UploadFile = File(...),
    sample_rate: int = 5,
    max_frames: int = None,
    db: Session = Depends(get_db)
):
    """
    Detect hand keypoints from uploaded video file

    **INPUT:**
    - file: Video file (mp4, avi, mov, mkv)
    - sample_rate: Process 1 frame every N frames (default: 5)
    - max_frames: Maximum frames to process (default: None = all frames)

    **OUTPUT:**
    - success: bool
    - data:
        - total_frames_processed: int
        - hands_detected_frames: int
        - sample_frames: list - Sample of frames with keypoint data
        - summary: dict - Summary statistics
        - processing_time: float

    **STUDENT TODO:**
    This is a basic implementation showing hand keypoint extraction.
    Students can enhance this to:
    - Add gesture recognition from keypoint sequences
    - Generate gesture probability scores
    - Create gesture timeline visualization
    - Export keypoints to JSON/CSV for analysis
    """
    try:
        start_time = time.time()

        # Validate file extension
        if not validate_file_extension(file.filename, settings.ALLOWED_VIDEO_EXTENSIONS):
            return create_response(
                success=False,
                message="Invalid file extension",
                error=f"Allowed: {', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)}"
            )

        # Save uploaded file
        file_content = await file.read()
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            return create_response(
                success=False,
                message="File too large",
                error=f"Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024):.0f}MB"
            )

        file_path = save_uploaded_file(
            file_content,
            file.filename,
            settings.RAW_DATA_DIR / "videos"
        )

        # Process video and extract hand keypoints
        result = service.process_video_hand_keypoints(
            str(file_path),
            sample_rate=sample_rate,
            max_frames=max_frames
        )

        processing_time = time.time() - start_time
        result['processing_time'] = processing_time

        return create_response(
            success=result['success'],
            message="Video processed successfully" if result['success'] else "Processing failed",
            data=result
        )

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            message="Error processing video",
            error=str(e)
        )


@router.websocket("/hand-tracking/realtime")
async def hand_tracking_realtime(websocket: WebSocket):
    """
    WebSocket endpoint for real-time hand keypoint detection

    **PURPOSE:**
    Real-time hand tracking using MediaPipe Hands.
    Frontend sends camera frames, backend returns hand keypoint locations.

    **PROTOCOL:**
    - Frontend sends: base64-encoded JPEG frames
    - Backend sends: JSON with hand keypoint coordinates

    **OUTPUT FORMAT:**
    {
        'success': bool,
        'hands_detected': int,
        'hands': [
            {
                'hand_type': 'Left' | 'Right',
                'keypoints': [
                    {'x': float, 'y': float, 'z': float, 'id': int},
                    ...  # 21 keypoints per hand
                ]
            }
        ],
        'timestamp': float
    }

    **USAGE:**
    - Connect via WebSocket: ws://localhost:8000/api/v1/vsl/hand-tracking/realtime
    - Send base64-encoded frame as text message
    - Receive JSON response with keypoint data

    **NOTE:**
    - This is a basic implementation for students to build upon
    - Optimized for educational purposes, showing keypoint locations in real-time
    """
    await websocket.accept()
    logger.info("[WebSocket] Hand tracking client connected")

    try:
        while True:
            # Receive frame data from frontend (base64-encoded image)
            data = await websocket.receive_text()

            try:
                # Process frame and detect hand keypoints
                result = service.detect_hand_keypoints_realtime(data)

                # Print keypoints to console for debugging
                if result['success'] and result['hands_detected'] > 0:
                    logger.info(f"[Hand Tracking] Detected {result['hands_detected']} hand(s)")
                    for hand in result['hands']:
                        logger.info(f"  - {hand['hand_type']} hand: {len(hand['keypoints'])} keypoints")
                        # Print first 3 keypoints as example
                        for i, kp in enumerate(hand['keypoints'][:3]):
                            logger.info(f"    Point {i}: x={kp['x']:.3f}, y={kp['y']:.3f}, z={kp['z']:.3f}")

                # Send result back to frontend
                await websocket.send_json(result)

            except Exception as e:
                logger.error(f"[WebSocket] Error processing frame: {str(e)}")
                error_response = {
                    'success': False,
                    'hands_detected': 0,
                    'hands': [],
                    'error': str(e),
                    'timestamp': time.time()
                }
                await websocket.send_json(error_response)

    except WebSocketDisconnect:
        logger.info("[WebSocket] Hand tracking client disconnected")
    except Exception as e:
        logger.error(f"[WebSocket] Unexpected error: {str(e)}", exc_info=True)
