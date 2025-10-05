"""
Core Utility Functions
Các hàm tiện ích dùng chung cho toàn bộ ứng dụng
"""
import os
import cv2
import numpy as np
import logging
from pathlib import Path
from typing import Optional, Tuple, Union
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Kiểm tra file extension có hợp lệ không

    INPUT:
        filename: Tên file (vd: "video.mp4")
        allowed_extensions: Set các extensions cho phép (vd: {".mp4", ".avi"})
    OUTPUT:
        bool: True nếu extension hợp lệ
    """
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions


def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """
    Tạo tên file unique dựa trên timestamp và hash

    INPUT:
        original_filename: Tên file gốc
        prefix: Prefix cho tên file (optional)
    OUTPUT:
        str: Tên file unique (vd: "prefix_20240101_120000_abc123.mp4")
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = Path(original_filename).suffix
    hash_str = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]

    if prefix:
        return f"{prefix}_{timestamp}_{hash_str}{ext}"
    return f"{timestamp}_{hash_str}{ext}"


def save_uploaded_file(file_content: bytes, filename: str, save_dir: Path) -> str:
    """
    Lưu uploaded file vào thư mục

    INPUT:
        file_content: Binary content của file
        filename: Tên file
        save_dir: Thư mục lưu file
    OUTPUT:
        str: Đường dẫn đầy đủ đến file đã lưu
    RAISES:
        Exception nếu không lưu được file
    """
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        unique_filename = generate_unique_filename(filename)
        file_path = save_dir / unique_filename

        with open(file_path, "wb") as f:
            f.write(file_content)

        logger.info(f"File saved: {file_path}")
        return str(file_path)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise


def load_image(image_path: Union[str, Path]) -> Optional[np.ndarray]:
    """
    Load image từ file

    INPUT:
        image_path: Đường dẫn đến image file
    OUTPUT:
        numpy array (BGR format) hoặc None nếu lỗi
    """
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
        return image
    except Exception as e:
        logger.error(f"Error loading image: {str(e)}")
        return None


def save_image(image: np.ndarray, save_path: Union[str, Path]) -> bool:
    """
    Lưu image vào file

    INPUT:
        image: numpy array (BGR format)
        save_path: Đường dẫn lưu image
    OUTPUT:
        bool: True nếu lưu thành công
    """
    try:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        success = cv2.imwrite(str(save_path), image)
        if success:
            logger.info(f"Image saved: {save_path}")
        return success
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return False


def resize_image(
    image: np.ndarray,
    width: Optional[int] = None,
    height: Optional[int] = None,
    maintain_aspect_ratio: bool = True
) -> np.ndarray:
    """
    Resize image

    INPUT:
        image: numpy array
        width: Target width (optional)
        height: Target height (optional)
        maintain_aspect_ratio: Giữ tỷ lệ khung hình
    OUTPUT:
        numpy array: Image đã resize
    NOTE: Phải cung cấp ít nhất width hoặc height
    """
    h, w = image.shape[:2]

    if width is None and height is None:
        return image

    if maintain_aspect_ratio:
        if width is not None and height is None:
            ratio = width / w
            height = int(h * ratio)
        elif height is not None and width is None:
            ratio = height / h
            width = int(w * ratio)

    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


def extract_frames_from_video(
    video_path: Union[str, Path],
    sample_rate: int = 1,
    max_frames: Optional[int] = None
) -> list:
    """
    Trích xuất frames từ video

    INPUT:
        video_path: Đường dẫn đến video file
        sample_rate: Lấy 1 frame mỗi N frames (default: 1 = lấy tất cả)
        max_frames: Số frames tối đa (optional)
    OUTPUT:
        list of numpy arrays (frames)
    RAISES:
        Exception nếu không đọc được video
    """
    try:
        cap = cv2.VideoCapture(str(video_path))
        frames = []
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % sample_rate == 0:
                frames.append(frame)

                if max_frames and len(frames) >= max_frames:
                    break

            frame_count += 1

        cap.release()
        logger.info(f"Extracted {len(frames)} frames from video")
        return frames
    except Exception as e:
        logger.error(f"Error extracting frames: {str(e)}")
        raise


def get_video_info(video_path: Union[str, Path]) -> dict:
    """
    Lấy thông tin về video

    INPUT:
        video_path: Đường dẫn đến video file
    OUTPUT:
        {
            'width': int,
            'height': int,
            'fps': float,
            'frame_count': int,
            'duration': float (seconds)
        }
    """
    try:
        cap = cv2.VideoCapture(str(video_path))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0

        cap.release()

        return {
            'width': width,
            'height': height,
            'fps': fps,
            'frame_count': frame_count,
            'duration': duration
        }
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise


def calculate_distance(point1: dict, point2: dict) -> float:
    """
    Tính khoảng cách Euclidean giữa 2 điểm

    INPUT:
        point1: {'x': float, 'y': float, 'z': float}
        point2: {'x': float, 'y': float, 'z': float}
    OUTPUT:
        float: Khoảng cách
    """
    dx = point1['x'] - point2['x']
    dy = point1['y'] - point2['y']
    dz = point1.get('z', 0) - point2.get('z', 0)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def normalize_landmarks(landmarks: list, reference_point: Optional[dict] = None) -> list:
    """
    Normalize landmarks về tọa độ tương đối

    INPUT:
        landmarks: List of {'x': float, 'y': float, 'z': float}
        reference_point: Điểm tham chiếu (optional, default: điểm đầu tiên)
    OUTPUT:
        list: Normalized landmarks
    """
    if not landmarks:
        return []

    if reference_point is None:
        reference_point = landmarks[0]

    normalized = []
    for lm in landmarks:
        normalized.append({
            'x': lm['x'] - reference_point['x'],
            'y': lm['y'] - reference_point['y'],
            'z': lm.get('z', 0) - reference_point.get('z', 0)
        })

    return normalized


def save_json(data: dict, file_path: Union[str, Path]) -> bool:
    """
    Lưu dictionary vào JSON file

    INPUT:
        data: Dictionary cần lưu
        file_path: Đường dẫn file
    OUTPUT:
        bool: True nếu lưu thành công
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON: {str(e)}")
        return False


def load_json(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Load JSON file

    INPUT:
        file_path: Đường dẫn file
    OUTPUT:
        dict hoặc None nếu lỗi
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON: {str(e)}")
        return None


def create_response(
    success: bool,
    message: str = "",
    data: Optional[dict] = None,
    error: Optional[str] = None
) -> dict:
    """
    Tạo standardized API response

    INPUT:
        success: bool
        message: Thông báo
        data: Dữ liệu trả về (optional)
        error: Thông tin lỗi (optional)
    OUTPUT:
        {
            'success': bool,
            'message': str,
            'data': dict or None,
            'error': str or None,
            'timestamp': str (ISO format)
        }
    """
    return {
        'success': success,
        'message': message,
        'data': data,
        'error': error,
        'timestamp': datetime.now().isoformat()
    }
