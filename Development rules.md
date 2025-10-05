# Development Rules - VSL Application
## Quy tắc phát triển cho dự án VSL Application

**Document Version:** 1.0.0
**Last Updated:** 2025-10-05
**Target Audience:** Student Developers

---

## Table of Contents / Mục lục

1. [Code Organization Rules](#1-code-organization-rules)
2. [Error Handling](#2-error-handling)
3. [API Development Rules](#3-api-development-rules)
4. [Function Documentation](#4-function-documentation)
5. [Git Workflow](#5-git-workflow)
6. [Testing Requirements](#6-testing-requirements)
7. [Helper/Utils Guidelines](#7-helperutils-guidelines)
8. [Database Rules](#8-database-rules)
9. [Frontend Development Rules](#9-frontend-development-rules)
10. [Code Quality](#10-code-quality)

---

## 1. Code Organization Rules
## Quy tắc tổ chức code

### 1.1 File Size Limit / Giới hạn kích thước file

**RULE:** Mỗi file không được vượt quá **800 dòng code**

**Lý do:**
- Dễ đọc, dễ maintain
- Tránh merge conflicts
- Cải thiện performance khi load file

**Example:**
```python
# ❌ BAD - file quá lớn
# vsl_service.py (1500 lines)
def recognize_video():
    # 500 lines
    pass

def recognize_image():
    # 500 lines
    pass

def process_landmarks():
    # 500 lines
    pass

# ✅ GOOD - tách thành nhiều files
# vsl_service.py (300 lines)
from .video_processor import recognize_video
from .image_processor import recognize_image
from .landmark_processor import process_landmarks

# video_processor.py (250 lines)
def recognize_video():
    pass

# image_processor.py (250 lines)
def recognize_image():
    pass

# landmark_processor.py (250 lines)
def process_landmarks():
    pass
```

### 1.2 How to Split Large Files / Cách tách file lớn

**Khi nào cần tách file:**
- File > 800 dòng
- File có nhiều hơn 10 functions không liên quan
- Có nhiều class trong 1 file
- Code khó tìm kiếm

**Cách tách:**

**Step 1:** Phân nhóm các functions theo chức năng
```python
# Before: service.py (1000 lines)
def video_function_1():
    pass
def video_function_2():
    pass
def image_function_1():
    pass
def image_function_2():
    pass
```

**Step 2:** Tạo file mới cho mỗi nhóm
```
modules/vsl_recognition/
├── service.py           # Main service (import & delegate)
├── video_service.py     # Video-related functions
├── image_service.py     # Image-related functions
└── utils.py            # Helper functions
```

**Step 3:** Import và expose functions
```python
# service.py
from .video_service import (
    recognize_from_video,
    process_video_frames
)
from .image_service import (
    recognize_from_image,
    process_single_image
)

# Expose functions cho external import
__all__ = [
    'recognize_from_video',
    'recognize_from_image',
    'process_video_frames',
    'process_single_image'
]
```

**Step 4:** Update imports trong các file khác
```python
# router.py
# Before:
from . import service
result = service.recognize_from_video(path)

# After: (vẫn hoạt động vì service.py expose functions)
from . import service
result = service.recognize_from_video(path)

# Hoặc import trực tiếp:
from .video_service import recognize_from_video
result = recognize_from_video(path)
```

### 1.3 Naming Conventions / Quy tắc đặt tên

#### Backend (Python)

```python
# Files & Modules: snake_case
vsl_recognition_service.py
model_manager.py

# Classes: PascalCase
class ModelManager:
    pass

class VSLRecognitionService:
    pass

# Functions & Variables: snake_case
def recognize_from_video():
    pass

user_data = {}
max_confidence = 0.95

# Constants: UPPER_SNAKE_CASE
MAX_UPLOAD_SIZE = 100 * 1024 * 1024
API_VERSION = "v1"

# Private functions/methods: leading underscore
def _internal_helper():
    pass

class MyClass:
    def _private_method(self):
        pass
```

#### Frontend (JavaScript/React)

```javascript
// Files: PascalCase for components, camelCase for utilities
CameraToText.jsx
Layout.jsx
api.js
utils.js

// Components: PascalCase
function CameraToText() {
  return <div>...</div>
}

// Functions & Variables: camelCase
const handleVideoUpload = () => {}
const userData = {}

// Constants: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 100 * 1024 * 1024
const API_BASE_URL = "http://localhost:8000"

// Hooks: camelCase with 'use' prefix
const useVideoProcessor = () => {}
```

### 1.4 Directory Structure Rules / Quy tắc cấu trúc thư mục

**Backend Module Structure:**
```
modules/
├── vsl_recognition/          # Module name (snake_case)
│   ├── __init__.py          # Export main functions
│   ├── router.py            # API endpoints ONLY
│   ├── service.py           # Business logic
│   ├── models.py            # ML models
│   ├── utils.py             # Helper functions
│   └── schemas.py           # Pydantic schemas (if needed)
```

**File Responsibilities:**

| File | Purpose | Max Lines | Content |
|------|---------|-----------|---------|
| `router.py` | API endpoints | 300 | Endpoints, request validation, response formatting |
| `service.py` | Business logic | 600 | Core functionality, coordination |
| `models.py` | ML models | 500 | Model loading, prediction |
| `utils.py` | Helpers | 400 | Utility functions specific to module |
| `schemas.py` | Data schemas | 200 | Pydantic models for validation |

**Frontend Component Structure:**
```
components/
├── common/                   # Shared components
│   ├── Layout.jsx
│   ├── Header.jsx
│   └── Footer.jsx
├── vsl-camera/              # Feature-specific
│   ├── CameraView.jsx
│   ├── CameraControls.jsx
│   └── VideoPreview.jsx
└── vsl-player/
    ├── AvatarPlayer.jsx
    └── PlayerControls.jsx
```

---

## 2. Error Handling
## Xử lý lỗi

### 2.1 Try-Catch Requirements / Yêu cầu Try-Catch

**RULE:** Tất cả functions có thể gây lỗi PHẢI có try-catch

**Functions cần try-catch:**
- File I/O operations
- Network requests
- Database operations
- External API calls
- Model predictions
- Image/Video processing

**Example:**

```python
# ❌ BAD - Không có error handling
def load_model(model_path):
    model = torch.load(model_path)
    return model

# ✅ GOOD - Có proper error handling
def load_model(model_path):
    """
    Load ML model từ file

    INPUT:
        model_path: str - Đường dẫn đến model file
    OUTPUT:
        Model object hoặc None nếu lỗi
    RAISES:
        FileNotFoundError: Nếu file không tồn tại
        RuntimeError: Nếu model không load được
    """
    try:
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        model = torch.load(model_path)
        logger.info(f"Model loaded successfully: {model_path}")
        return model

    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to load model: {str(e)}")
```

### 2.2 Error Logging Standards / Chuẩn ghi log lỗi

**Logging Levels:**

```python
import logging
logger = logging.getLogger(__name__)

# DEBUG: Thông tin chi tiết cho debugging
logger.debug(f"Processing frame {frame_count}")

# INFO: Thông tin hoạt động bình thường
logger.info("Model loaded successfully")
logger.info(f"Processed {len(results)} items")

# WARNING: Cảnh báo nhưng vẫn hoạt động được
logger.warning("Low confidence detection: 0.45")
logger.warning("Using default model - custom model not found")

# ERROR: Lỗi nghiêm trọng
logger.error(f"Failed to process video: {str(e)}")
logger.error("Database connection failed", exc_info=True)

# CRITICAL: Lỗi rất nghiêm trọng, có thể crash app
logger.critical("Out of memory - cannot continue")
```

**Best Practices:**

```python
# ✅ GOOD - Log đầy đủ thông tin
try:
    result = process_video(video_path)
    logger.info(f"Video processed: {video_path}, frames: {result['frame_count']}")

except FileNotFoundError as e:
    logger.error(f"Video file not found: {video_path}")
    raise

except Exception as e:
    logger.error(
        f"Error processing video: {video_path}",
        exc_info=True,  # Include full stack trace
        extra={
            'video_path': video_path,
            'error_type': type(e).__name__
        }
    )
    raise

# ❌ BAD - Log không đủ thông tin
try:
    result = process_video(video_path)
except:
    logger.error("Error")  # Quá chung chung, không biết lỗi gì
```

### 2.3 Error Response Format / Format phản hồi lỗi

**API Error Response Standard:**

```python
from ...core.utils import create_response

# ✅ Success Response
return create_response(
    success=True,
    message="Video processed successfully",
    data={
        'detected_text': "Xin chào",
        'confidence': 0.95,
        'frame_count': 120
    }
)

# ✅ Error Response
return create_response(
    success=False,
    message="Failed to process video",
    error="Invalid file format. Expected mp4, got avi"
)

# Response format:
{
    "success": bool,
    "message": str,
    "data": dict or None,
    "error": str or None,
    "timestamp": "2025-10-05T10:30:00"
}
```

**Error Categories:**

```python
# Validation Error - 400
return create_response(
    success=False,
    message="Validation error",
    error="File size exceeds maximum limit (100MB)"
)

# Not Found - 404
return create_response(
    success=False,
    message="Resource not found",
    error="Model file not found: vsl_recognition.pth"
)

# Processing Error - 500
return create_response(
    success=False,
    message="Processing error",
    error="Failed to extract landmarks from video"
)
```

### 2.4 Async Error Handling / Xử lý lỗi bất đồng bộ

```python
# Backend - FastAPI async endpoints
@router.post("/recognize-video")
async def recognize_video(file: UploadFile = File(...)):
    """
    Async endpoint with proper error handling
    """
    try:
        # Validate file
        if not validate_file_extension(file.filename, ALLOWED_EXTENSIONS):
            return create_response(
                success=False,
                message="Invalid file type",
                error=f"Allowed extensions: {ALLOWED_EXTENSIONS}"
            )

        # Read file content (async)
        file_content = await file.read()

        # Save file
        file_path = save_uploaded_file(file_content, file.filename, SAVE_DIR)

        # Process (this is blocking - consider running in thread pool)
        result = service.recognize_from_video(file_path)

        return create_response(
            success=True,
            message="Processing completed",
            data=result
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_response(
            success=False,
            message="Validation error",
            error=str(e)
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            message="Internal server error",
            error=str(e) if settings.DEBUG else "An error occurred"
        )
```

**Frontend - Async/Await:**

```javascript
// ✅ GOOD - Proper error handling
const handleVideoUpload = async (file) => {
  try {
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/v1/vsl/recognize-video', formData)

    if (response.data.success) {
      setResult(response.data.data)
      showNotification('Processing completed', 'success')
    } else {
      throw new Error(response.data.error || 'Processing failed')
    }

  } catch (error) {
    console.error('Error uploading video:', error)

    // User-friendly error messages
    if (error.response?.status === 413) {
      setError('File size too large. Maximum 100MB allowed.')
    } else if (error.response?.status === 400) {
      setError(error.response.data.error || 'Invalid file format')
    } else if (error.response?.status >= 500) {
      setError('Server error. Please try again later.')
    } else {
      setError(error.message || 'An error occurred')
    }

    showNotification('Upload failed', 'error')

  } finally {
    setLoading(false)
  }
}

// ❌ BAD - Không xử lý lỗi
const handleVideoUpload = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/api/v1/vsl/recognize-video', formData)
  setResult(response.data.data)  // Sẽ crash nếu có lỗi
}
```

---

## 3. API Development Rules
## Quy tắc phát triển API

### 3.1 Input Validation Requirements / Yêu cầu validate input

**RULE:** Validate TẤT CẢ inputs trước khi xử lý

**Validation Checklist:**
- [ ] File extension
- [ ] File size
- [ ] Required parameters
- [ ] Data types
- [ ] Value ranges
- [ ] Format (email, URL, etc.)

**Example:**

```python
from fastapi import UploadFile, File, HTTPException
from ...core.utils import validate_file_extension, create_response
from ...config import settings

@router.post("/recognize-video")
async def recognize_video(
    file: UploadFile = File(...),
    confidence_threshold: float = 0.5,
    max_frames: int = None
):
    """
    Endpoint with comprehensive input validation
    """
    # 1. Validate file extension
    if not validate_file_extension(file.filename, settings.ALLOWED_VIDEO_EXTENSIONS):
        return create_response(
            success=False,
            message="Invalid file extension",
            error=f"Allowed: {', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)}"
        )

    # 2. Validate file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_UPLOAD_SIZE:
        return create_response(
            success=False,
            message="File too large",
            error=f"Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
        )

    # 3. Validate parameters
    if not 0.0 <= confidence_threshold <= 1.0:
        return create_response(
            success=False,
            message="Invalid parameter",
            error="confidence_threshold must be between 0.0 and 1.0"
        )

    if max_frames is not None and max_frames <= 0:
        return create_response(
            success=False,
            message="Invalid parameter",
            error="max_frames must be positive"
        )

    # 4. Process after validation
    try:
        file_path = save_uploaded_file(file_content, file.filename, SAVE_DIR)
        result = service.recognize_from_video(
            file_path,
            options={
                'confidence_threshold': confidence_threshold,
                'max_frames': max_frames
            }
        )
        return create_response(success=True, message="Success", data=result)

    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            message="Processing failed",
            error=str(e)
        )
```

**Using Pydantic for Validation:**

```python
from pydantic import BaseModel, Field, validator

class VideoRecognitionRequest(BaseModel):
    confidence_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence threshold (0.0-1.0)"
    )
    max_frames: Optional[int] = Field(
        default=None,
        gt=0,
        description="Maximum frames to process"
    )
    sample_rate: int = Field(
        default=5,
        gt=0,
        le=30,
        description="Sample rate (frames)"
    )

    @validator('max_frames')
    def validate_max_frames(cls, v):
        if v is not None and v > 10000:
            raise ValueError('max_frames cannot exceed 10000')
        return v

@router.post("/recognize-video")
async def recognize_video(
    file: UploadFile = File(...),
    params: VideoRecognitionRequest = Depends()
):
    # params is automatically validated by Pydantic
    pass
```

### 3.2 Output Format Standards / Chuẩn format output

**Standard Response Structure:**

```python
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Actual data here
    },
    "error": null,
    "timestamp": "2025-10-05T10:30:00.000Z"
}
```

**Examples:**

```python
# List Response
{
    "success": true,
    "message": "Gestures retrieved",
    "data": {
        "gestures": [
            {"id": 1, "name": "Chào", "category": "greeting"},
            {"id": 2, "name": "Cảm ơn", "category": "gratitude"}
        ],
        "total": 2
    }
}

# Single Object Response
{
    "success": true,
    "message": "Video processed",
    "data": {
        "detected_text": "Xin chào",
        "confidence": 0.95,
        "frame_count": 120,
        "processing_time": 2.5
    }
}

# Pagination Response
{
    "success": true,
    "message": "Data retrieved",
    "data": {
        "items": [...],
        "total": 100,
        "page": 1,
        "page_size": 20,
        "total_pages": 5
    }
}

# Error Response
{
    "success": false,
    "message": "Processing failed",
    "data": null,
    "error": "Invalid file format",
    "timestamp": "2025-10-05T10:30:00.000Z"
}
```

### 3.3 HTTP Status Codes / Mã trạng thái HTTP

**Use Correct Status Codes:**

```python
from fastapi import status

# 200 OK - Success
return JSONResponse(
    status_code=status.HTTP_200_OK,
    content=create_response(success=True, message="Success", data=result)
)

# 201 Created - Resource created
return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content=create_response(success=True, message="Created", data=new_resource)
)

# 400 Bad Request - Invalid input
return JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=create_response(success=False, error="Invalid parameters")
)

# 404 Not Found - Resource not found
return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content=create_response(success=False, error="Resource not found")
)

# 500 Internal Server Error - Server error
return JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content=create_response(success=False, error="Internal error")
)
```

**Status Code Guide:**

| Code | Name | When to Use |
|------|------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | New resource created |
| 204 | No Content | Success, no response body |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 413 | Payload Too Large | File size exceeded |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Temporary unavailable |

### 3.4 CORS Handling / Xử lý CORS

**Backend Configuration:**

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Or specific: ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # Or specific headers
)

# config.py
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
```

**Frontend Configuration:**

```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true  // Allow cookies
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if needed
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

---

## 4. Function Documentation
## Tài liệu hóa hàm

### 4.1 INPUT/OUTPUT Documentation Format

**REQUIRED for ALL functions:**

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Mô tả ngắn gọn chức năng của hàm (1-2 dòng)

    Mô tả chi tiết hơn nếu cần (optional)

    INPUT:
        param1: type - Mô tả parameter 1
        param2: type - Mô tả parameter 2
            - sub_option1: Mô tả option (nếu là dict)
            - sub_option2: Mô tả option

    OUTPUT:
        return_type - Mô tả output
        {
            'key1': type - Mô tả,
            'key2': type - Mô tả
        }

    RAISES: (optional)
        ExceptionType: Khi nào raise exception này

    USAGE: (optional)
        Example code showing how to use

    NOTE: (optional)
        Các lưu ý quan trọng
    """
    pass
```

**Real Examples:**

```python
def extract_frames_from_video(
    video_path: Union[str, Path],
    sample_rate: int = 1,
    max_frames: Optional[int] = None
) -> list:
    """
    Trích xuất frames từ video file

    Function này đọc video và extract frames theo tỷ lệ sample_rate.
    Hữu ích cho preprocessing video trước khi nhận diện VSL.

    INPUT:
        video_path: str or Path - Đường dẫn đến video file
        sample_rate: int - Lấy 1 frame mỗi N frames (default: 1 = lấy tất cả)
        max_frames: int or None - Số frames tối đa muốn extract (default: None = không giới hạn)

    OUTPUT:
        list of numpy.ndarray - Danh sách frames (BGR format)
        Mỗi frame là numpy array shape (height, width, 3)

    RAISES:
        FileNotFoundError: Nếu video file không tồn tại
        ValueError: Nếu không thể đọc được video

    USAGE:
        # Extract all frames
        frames = extract_frames_from_video('video.mp4')

        # Extract every 5th frame
        frames = extract_frames_from_video('video.mp4', sample_rate=5)

        # Extract max 100 frames
        frames = extract_frames_from_video('video.mp4', max_frames=100)

    NOTE:
        - Video phải ở format được OpenCV hỗ trợ (mp4, avi, mov, mkv)
        - Memory usage: ~1MB per frame (1080p)
    """
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

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
        logger.info(f"Extracted {len(frames)} frames from {video_path}")
        return frames

    except Exception as e:
        logger.error(f"Error extracting frames: {str(e)}")
        raise
```

**For Service Functions:**

```python
def recognize_from_video(video_path: str, options: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Nhận diện VSL từ video file

    INPUT:
        video_path: str - Đường dẫn đến video file
        options: dict or None - Các tùy chọn:
            - sample_rate: int - Lấy 1 frame mỗi N frames (default: 5)
            - confidence_threshold: float - Ngưỡng confidence (default: 0.5)
            - max_frames: int - Số frames tối đa xử lý (default: None)

    OUTPUT:
        {
            'success': bool - True nếu xử lý thành công,
            'detected_text': str - Text được nhận diện từ VSL,
            'confidence': float - Độ tin cậy trung bình (0-1),
            'frame_count': int - Số frames đã xử lý,
            'landmarks_sequence': list - Sequence of landmarks (optional),
            'processing_time': float - Thời gian xử lý (seconds),
            'error': str or None - Thông báo lỗi nếu có
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
        if result['success']:
            print(f"Detected: {result['detected_text']}")
            print(f"Confidence: {result['confidence']:.2f}")
    """
    # Implementation
    pass
```

### 4.2 Docstring Requirements / Yêu cầu docstring

**ALL functions MUST have docstrings với:**

1. **Brief description** - 1-2 dòng mô tả chức năng
2. **INPUT** - Mô tả tất cả parameters
3. **OUTPUT** - Mô tả return value
4. **RAISES** - Liệt kê exceptions (nếu có)
5. **USAGE/EXAMPLE** - Example code (recommended)
6. **NOTE** - Lưu ý quan trọng (nếu cần)

**Classes:**

```python
class ModelManager:
    """
    Singleton class quản lý các shared models (MediaPipe, OpenCV, etc.)

    Class này cache các models trong memory để tái sử dụng,
    tránh load model nhiều lần và tối ưu hiệu năng.

    USAGE:
        manager = ModelManager()
        hands_model = manager.get_hands_model()
        results = hands_model.process(image)

    NOTE:
        - Singleton pattern: chỉ có 1 instance duy nhất
        - Thread-safe
        - Auto-cleanup khi shutdown
    """

    def __init__(self):
        """Initialize model manager"""
        self._models = {}
        self._initialize_models()
```

**Frontend Functions (JSDoc):**

```javascript
/**
 * Upload video file và nhận diện VSL
 *
 * @param {File} file - Video file object
 * @param {Object} options - Upload options
 * @param {number} options.confidenceThreshold - Confidence threshold (0-1)
 * @param {number} options.maxFrames - Maximum frames to process
 *
 * @returns {Promise<Object>} Recognition result
 * @returns {boolean} returns.success - Success status
 * @returns {string} returns.detectedText - Detected VSL text
 * @returns {number} returns.confidence - Confidence score
 *
 * @throws {Error} If file is invalid or upload fails
 *
 * @example
 * const result = await uploadVideo(videoFile, { confidenceThreshold: 0.7 })
 * console.log(result.detectedText)
 */
async function uploadVideo(file, options = {}) {
  // Implementation
}
```

### 4.3 Example Usage / Ví dụ sử dụng

**ALWAYS include examples:**

```python
def calculate_similarity(landmarks1: list, landmarks2: list) -> float:
    """
    Tính độ tương đồng giữa 2 sets of landmarks

    INPUT:
        landmarks1: list of dict - Landmarks set 1
        landmarks2: list of dict - Landmarks set 2
            Each landmark: {'x': float, 'y': float, 'z': float}

    OUTPUT:
        float - Similarity score (0-1), 1 = giống hệt

    USAGE:
        # Compare hand landmarks
        lm1 = [{'x': 0.5, 'y': 0.3, 'z': 0.1}, ...]
        lm2 = [{'x': 0.51, 'y': 0.29, 'z': 0.11}, ...]
        similarity = calculate_similarity(lm1, lm2)

        if similarity > 0.8:
            print("Gestures are similar")

    ALGORITHM:
        Sử dụng cosine similarity trên normalized vectors
    """
    pass
```

---

## 5. Git Workflow
## Quy trình làm việc với Git

### 5.1 Branch Naming Conventions / Quy tắc đặt tên branch

**Format:**
```
<type>/<short-description>
```

**Types:**
- `feature/` - Tính năng mới
- `fix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Tests
- `chore/` - Maintenance tasks

**Examples:**
```bash
feature/vsl-recognition-video
feature/audio-to-text-whisper
fix/video-upload-timeout
fix/landmark-extraction-error
refactor/split-large-service-file
docs/api-documentation
test/add-unit-tests-vsl-service
chore/update-dependencies
```

**Rules:**
- Lowercase only
- Use hyphens, not underscores
- Keep it short but descriptive
- Max 50 characters

### 5.2 Commit Message Format / Format commit message

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting, missing semicolons, etc
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `test` - Adding tests
- `chore` - Maintenance

**Examples:**

```bash
# Good commit messages
feat(vsl): add video recognition endpoint
fix(api): handle empty landmarks in gesture detection
docs(readme): update setup instructions
refactor(service): split large file into modules
test(vsl): add unit tests for landmark extraction

# With body
feat(speech): implement speech-to-text with Whisper

- Integrate OpenAI Whisper model
- Support Vietnamese language
- Add audio preprocessing
- Handle various audio formats

Closes #123

# Bad commit messages (DON'T DO THIS)
update code
fix bug
changes
wip
asdasd
```

**Rules:**
- Subject line max 72 characters
- Use imperative mood ("add" not "added")
- Don't end subject with period
- Separate subject from body with blank line
- Use body to explain WHAT and WHY, not HOW

### 5.3 Pull Request Process / Quy trình Pull Request

**Before Creating PR:**

```bash
# 1. Update your branch with latest main
git checkout main
git pull origin main
git checkout your-feature-branch
git merge main

# 2. Run tests
pytest tests/

# 3. Run linter
flake8 .
black .

# 4. Check for merge conflicts
# Resolve any conflicts

# 5. Push to remote
git push origin your-feature-branch
```

**PR Title Format:**
```
[TYPE] Short description of changes
```

Examples:
```
[FEATURE] Add VSL video recognition endpoint
[FIX] Resolve timeout issue in video upload
[REFACTOR] Split service.py into multiple files
[DOCS] Add API documentation
```

**PR Description Template:**

```markdown
## Summary / Tóm tắt
Brief description of what this PR does

## Changes / Thay đổi
- Added video recognition endpoint
- Implemented landmark extraction
- Updated tests

## Related Issues / Issues liên quan
Closes #123
Relates to #456

## Testing / Kiểm thử
- [ ] Unit tests added
- [ ] Integration tests passed
- [ ] Manual testing completed

## Screenshots / Ảnh chụp màn hình (if applicable)
[Add screenshots here]

## Checklist / Danh sách kiểm tra
- [ ] Code follows project coding standards
- [ ] All functions have proper documentation
- [ ] No files exceed 800 lines
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] README/docs updated (if needed)
```

### 5.4 Code Review Checklist / Danh sách kiểm tra code review

**Reviewer phải kiểm tra:**

**Code Quality:**
- [ ] Code dễ đọc, dễ hiểu
- [ ] Tên biến/hàm có ý nghĩa
- [ ] Không có code duplicate
- [ ] Không có magic numbers (dùng constants)
- [ ] Functions không quá dài (< 50 lines)
- [ ] Files không quá 800 lines

**Documentation:**
- [ ] Tất cả functions có docstring
- [ ] Docstring có INPUT/OUTPUT format
- [ ] Có example usage
- [ ] README updated nếu cần

**Error Handling:**
- [ ] Có try-catch cho operations nguy hiểm
- [ ] Error logging đầy đủ
- [ ] Error messages rõ ràng
- [ ] Không có bare except

**Testing:**
- [ ] Có unit tests cho new code
- [ ] Tests cover edge cases
- [ ] Tất cả tests pass

**API (nếu có):**
- [ ] Input validation đầy đủ
- [ ] Response format chuẩn
- [ ] HTTP status codes đúng
- [ ] API documented

**Security:**
- [ ] Không có hardcoded credentials
- [ ] Input được sanitize
- [ ] File uploads được validate
- [ ] Không có SQL injection vulnerabilities

**Performance:**
- [ ] Không có performance bottlenecks
- [ ] Database queries optimized
- [ ] Large files handled properly

**Comments:**
```python
# Provide constructive feedback
# ✅ Good comment:
"Consider using a list comprehension here for better performance and readability"

# ✅ Good comment:
"This function is getting long. Can we extract lines 50-80 into a separate helper function?"

# ❌ Bad comment:
"This is bad code"

# ❌ Bad comment:
"Why did you do it this way?"
```

### 5.5 Merge Strategy / Chiến lược merge

**Squash and Merge** (Recommended for feature branches):
```bash
# Combines all commits into one clean commit
git checkout main
git merge --squash feature/my-feature
git commit -m "feat(module): add new feature"
```

**Merge Commit** (For long-running branches):
```bash
# Preserves commit history
git checkout main
git merge --no-ff feature/my-feature
```

**Rebase** (For keeping history linear):
```bash
# Use with caution
git checkout feature/my-feature
git rebase main
# Resolve conflicts
git push --force-with-lease
```

**Rules:**
- NEVER force push to `main` branch
- NEVER commit directly to `main` - always use PR
- Delete feature branch after merge
- Tag releases: `v1.0.0`, `v1.1.0`, etc.

---

## 6. Testing Requirements
## Yêu cầu kiểm thử

### 6.1 Unit Test Requirements / Yêu cầu unit test

**RULE:** Tất cả functions phải có unit tests

**Test Coverage Target:** Minimum 80%

**Test File Structure:**
```
backend/
├── app/
│   ├── modules/
│   │   └── vsl_recognition/
│   │       ├── service.py
│   │       └── router.py
│   └── tests/
│       └── modules/
│           └── vsl_recognition/
│               ├── test_service.py
│               └── test_router.py
```

**Example Unit Tests:**

```python
# tests/modules/vsl_recognition/test_service.py
import pytest
from app.modules.vsl_recognition import service
from app.core.model_manager import model_manager

class TestRecognizeFromVideo:
    """Test cases cho recognize_from_video function"""

    def test_recognize_valid_video(self):
        """Test nhận diện video hợp lệ"""
        # Arrange
        video_path = "tests/fixtures/sample_video.mp4"
        options = {'sample_rate': 5, 'confidence_threshold': 0.5}

        # Act
        result = service.recognize_from_video(video_path, options)

        # Assert
        assert result['success'] is True
        assert 'detected_text' in result
        assert result['confidence'] >= 0.0
        assert result['confidence'] <= 1.0
        assert result['frame_count'] > 0

    def test_recognize_invalid_video_path(self):
        """Test với video path không tồn tại"""
        # Arrange
        video_path = "non_existent_video.mp4"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            service.recognize_from_video(video_path)

    def test_recognize_with_invalid_options(self):
        """Test với options không hợp lệ"""
        # Arrange
        video_path = "tests/fixtures/sample_video.mp4"
        options = {'confidence_threshold': 1.5}  # Invalid: > 1.0

        # Act & Assert
        with pytest.raises(ValueError):
            service.recognize_from_video(video_path, options)

    @pytest.mark.parametrize("sample_rate,expected_min_frames", [
        (1, 100),
        (5, 20),
        (10, 10),
    ])
    def test_different_sample_rates(self, sample_rate, expected_min_frames):
        """Test với các sample rates khác nhau"""
        # Arrange
        video_path = "tests/fixtures/sample_video.mp4"
        options = {'sample_rate': sample_rate}

        # Act
        result = service.recognize_from_video(video_path, options)

        # Assert
        assert result['frame_count'] >= expected_min_frames


class TestDetectGesture:
    """Test cases cho detect_gesture function"""

    @pytest.fixture
    def sample_landmarks(self):
        """Fixture cung cấp sample landmarks"""
        return {
            'left_hand_landmarks': [
                {'x': 0.5, 'y': 0.3, 'z': 0.1} for _ in range(21)
            ],
            'right_hand_landmarks': None,
            'pose_landmarks': [
                {'x': 0.5, 'y': 0.5, 'z': 0.0} for _ in range(33)
            ]
        }

    @pytest.fixture
    def sample_templates(self):
        """Fixture cung cấp sample gesture templates"""
        return [
            {'id': 1, 'name': 'Chào', 'keypoints': [...]}
        ]

    def test_detect_known_gesture(self, sample_landmarks, sample_templates):
        """Test detect gesture đã biết"""
        # Act
        result = service.detect_gesture(sample_landmarks, sample_templates)

        # Assert
        assert result['success'] is True
        assert result['gesture_name'] is not None
        assert result['confidence'] > 0.0

    def test_detect_with_empty_landmarks(self, sample_templates):
        """Test với landmarks rỗng"""
        # Arrange
        empty_landmarks = {
            'left_hand_landmarks': None,
            'right_hand_landmarks': None,
            'pose_landmarks': None
        }

        # Act
        result = service.detect_gesture(empty_landmarks, sample_templates)

        # Assert
        assert result['success'] is False
        assert result['gesture_name'] is None
```

**Frontend Tests (Jest + React Testing Library):**

```javascript
// src/components/__tests__/CameraToText.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import CameraToText from '../CameraToText'
import api from '../../services/api'

// Mock API
vi.mock('../../services/api')

describe('CameraToText Component', () => {
  it('renders camera view', () => {
    render(<CameraToText />)
    expect(screen.getByText(/VSL Recognition/i)).toBeInTheDocument()
  })

  it('handles video file upload', async () => {
    // Mock API response
    api.post.mockResolvedValue({
      data: {
        success: true,
        data: { detected_text: 'Xin chào', confidence: 0.95 }
      }
    })

    render(<CameraToText />)

    // Simulate file upload
    const file = new File(['video'], 'test.mp4', { type: 'video/mp4' })
    const input = screen.getByLabelText(/upload video/i)

    fireEvent.change(input, { target: { files: [file] } })

    // Wait for result
    await waitFor(() => {
      expect(screen.getByText(/Xin chào/i)).toBeInTheDocument()
      expect(screen.getByText(/0.95/i)).toBeInTheDocument()
    })
  })

  it('shows error on upload failure', async () => {
    // Mock API error
    api.post.mockRejectedValue(new Error('Upload failed'))

    render(<CameraToText />)

    const file = new File(['video'], 'test.mp4', { type: 'video/mp4' })
    const input = screen.getByLabelText(/upload video/i)

    fireEvent.change(input, { target: { files: [file] } })

    await waitFor(() => {
      expect(screen.getByText(/Upload failed/i)).toBeInTheDocument()
    })
  })
})
```

### 6.2 Integration Test Guidelines / Hướng dẫn integration test

**Integration tests** test sự tương tác giữa các modules

```python
# tests/integration/test_vsl_pipeline.py
import pytest
from app.modules.vsl_recognition import service as vsl_service
from app.core.model_manager import model_manager
from app.core import utils

class TestVSLRecognitionPipeline:
    """Test full VSL recognition pipeline"""

    @pytest.mark.integration
    def test_full_video_recognition_pipeline(self):
        """
        Test full pipeline:
        1. Upload video
        2. Extract frames
        3. Extract landmarks
        4. Recognize VSL
        5. Return result
        """
        # Arrange
        video_path = "tests/fixtures/integration/sample_vsl_video.mp4"

        # Act
        # Step 1: Extract frames
        frames = utils.extract_frames_from_video(video_path, sample_rate=5)
        assert len(frames) > 0

        # Step 2: Extract landmarks from first frame
        landmarks = model_manager.extract_holistic_landmarks(frames[0])
        assert landmarks['success'] is True

        # Step 3: Full recognition
        result = vsl_service.recognize_from_video(video_path)

        # Assert
        assert result['success'] is True
        assert result['detected_text'] != ""
        assert result['confidence'] > 0.0
        assert result['frame_count'] == len(frames)

    @pytest.mark.integration
    def test_api_endpoint_integration(self, test_client):
        """Test API endpoint with real processing"""
        # Upload video through API
        with open("tests/fixtures/sample_video.mp4", "rb") as f:
            response = test_client.post(
                "/api/v1/vsl/recognize-video",
                files={"file": ("video.mp4", f, "video/mp4")}
            )

        # Assert response
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'detected_text' in data['data']
```

### 6.3 Test File Naming / Quy tắc đặt tên test files

**Backend:**
```
test_<module_name>.py
test_<function_name>.py
```

Examples:
```
test_service.py
test_router.py
test_model_manager.py
test_utils.py
```

**Frontend:**
```
<ComponentName>.test.jsx
<fileName>.test.js
```

Examples:
```
CameraToText.test.jsx
api.test.js
utils.test.js
```

### 6.4 Running Tests / Chạy tests

**Backend:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/modules/vsl_recognition/test_service.py

# Run specific test
pytest tests/modules/vsl_recognition/test_service.py::TestRecognizeFromVideo::test_recognize_valid_video

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest -m "not integration"

# Run only integration tests
pytest -m integration

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

**Frontend:**
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run specific test file
npm test -- CameraToText.test.jsx
```

---

## 7. Helper/Utils Guidelines
## Hướng dẫn về Helper/Utils

### 7.1 When to Create Helper Functions / Khi nào tạo helper functions

**Create helper function when:**

1. **Code được lặp lại >= 3 lần**
```python
# ❌ BAD - Duplicate code
def process_video():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    # ...

def process_image():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpg"
    # ...

# ✅ GOOD - Extract to helper
def generate_timestamp_filename(prefix, extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def process_video():
    filename = generate_timestamp_filename("video", "mp4")
    # ...
```

2. **Function quá dài (> 50 lines)**
```python
# ❌ BAD - Too long
def recognize_from_video(video_path):
    # Extract frames (20 lines)
    # ...

    # Extract landmarks (30 lines)
    # ...

    # Predict (20 lines)
    # ...

# ✅ GOOD - Split into helpers
def recognize_from_video(video_path):
    frames = _extract_frames(video_path)
    landmarks = _extract_landmarks(frames)
    result = _predict_from_landmarks(landmarks)
    return result

def _extract_frames(video_path):
    # 20 lines
    pass

def _extract_landmarks(frames):
    # 30 lines
    pass

def _predict_from_landmarks(landmarks):
    # 20 lines
    pass
```

3. **Logic phức tạp cần tách riêng**
```python
# ✅ GOOD - Complex logic in separate function
def calculate_gesture_similarity(lm1, lm2):
    """Complex similarity calculation"""
    # Normalize landmarks
    norm_lm1 = _normalize_landmarks(lm1)
    norm_lm2 = _normalize_landmarks(lm2)

    # Calculate features
    features1 = _extract_features(norm_lm1)
    features2 = _extract_features(norm_lm2)

    # Compute similarity
    similarity = _cosine_similarity(features1, features2)
    return similarity
```

### 7.2 Where to Place Shared Code / Đặt shared code ở đâu

**Structure:**

```
app/
├── core/
│   └── utils.py              # Global utilities (dùng bởi tất cả modules)
│
└── modules/
    ├── vsl_recognition/
    │   ├── service.py
    │   └── utils.py          # Module-specific utilities
    │
    └── speech_processing/
        ├── service.py
        └── utils.py          # Module-specific utilities
```

**Decision Tree:**

```
Is utility used by multiple modules?
├── YES → Put in core/utils.py
│   Examples:
│   - save_uploaded_file()
│   - generate_unique_filename()
│   - create_response()
│   - load_image()
│
└── NO → Put in module/utils.py
    Examples:
    - extract_hand_features()  (only for vsl_recognition)
    - preprocess_audio()       (only for speech_processing)
    - generate_gloss()         (only for text_to_vsl)
```

**Examples:**

```python
# core/utils.py - Global utilities
def save_uploaded_file(file_content: bytes, filename: str, save_dir: Path) -> str:
    """Used by ALL modules that handle file uploads"""
    pass

def create_response(success: bool, message: str, data: dict = None) -> dict:
    """Used by ALL API endpoints"""
    pass

def load_image(image_path: str) -> np.ndarray:
    """Used by vsl_recognition AND data_tools modules"""
    pass


# modules/vsl_recognition/utils.py - VSL-specific utilities
def normalize_hand_landmarks(landmarks: list) -> list:
    """Only used by vsl_recognition module"""
    pass

def calculate_hand_angle(p1: dict, p2: dict, p3: dict) -> float:
    """Only used by vsl_recognition module"""
    pass


# modules/speech_processing/utils.py - Speech-specific utilities
def preprocess_audio(audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
    """Only used by speech_processing module"""
    pass

def detect_voice_activity(audio_data: np.ndarray) -> list:
    """Only used by speech_processing module"""
    pass
```

### 7.3 How to Link Modules / Cách liên kết modules

**Import Hierarchy:**

```
Allowed imports:
✅ modules → core (modules can import from core)
✅ modules → database (modules can import from database)
✅ router → service (within same module)
✅ service → utils (within same module)

NOT allowed:
❌ core → modules (core should not depend on modules)
❌ modules → other modules (avoid cross-module dependencies)
```

**Good Practice:**

```python
# modules/vsl_recognition/service.py
from ...core.utils import save_uploaded_file, load_image
from ...core.model_manager import model_manager
from ...database.db import get_db
from .utils import normalize_hand_landmarks  # Module-specific util

def recognize_from_image(image_path: str):
    # Use core utility
    image = load_image(image_path)

    # Use core model manager
    landmarks = model_manager.extract_hand_landmarks(image)

    # Use module-specific utility
    normalized = normalize_hand_landmarks(landmarks['landmarks'])

    return result
```

**Bad Practice:**

```python
# ❌ BAD - Cross-module dependency
# modules/vsl_recognition/service.py
from ..speech_processing.utils import preprocess_audio  # DON'T DO THIS

# ✅ GOOD - Extract to core if needed by both
# core/utils.py
def preprocess_audio(audio_data):
    pass

# modules/vsl_recognition/service.py
from ...core.utils import preprocess_audio  # OK
```

### 7.4 Helper Function Best Practices / Best practices cho helper functions

**1. Single Responsibility**
```python
# ❌ BAD - Does too many things
def process_and_save_image(image_path, output_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (640, 480))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    landmarks = extract_landmarks(image)
    cv2.imwrite(output_path, image)
    return landmarks

# ✅ GOOD - Single responsibility
def resize_image(image, size):
    return cv2.resize(image, size)

def convert_color(image, conversion):
    return cv2.cvtColor(image, conversion)

def save_image(image, path):
    cv2.imwrite(path, image)
```

**2. Pure Functions (when possible)**
```python
# ✅ GOOD - Pure function (no side effects)
def normalize_landmarks(landmarks):
    """
    Pure function: same input always produces same output
    No side effects (no file I/O, no global state changes)
    """
    return [(lm['x'] - 0.5, lm['y'] - 0.5) for lm in landmarks]

# Sometimes side effects are necessary (file I/O, logging)
# Just document them clearly
def save_landmarks(landmarks, file_path):
    """
    SIDE EFFECTS: Writes to file system
    """
    with open(file_path, 'w') as f:
        json.dump(landmarks, f)
```

**3. Good Naming**
```python
# ✅ GOOD - Clear, descriptive names
def calculate_euclidean_distance(p1, p2):
    pass

def extract_hand_landmarks_from_image(image):
    pass

def validate_video_file_extension(filename):
    pass

# ❌ BAD - Unclear names
def calc(p1, p2):
    pass

def process(data):
    pass

def do_stuff(x):
    pass
```

---

## 8. Database Rules
## Quy tắc Database

### 8.1 Migration Procedures / Quy trình migration

**Database Structure:**
```
database/
├── vsl_app.db           # SQLite database file
├── migrations/          # Migration scripts (if using Alembic)
└── backups/            # Database backups
```

**Using Alembic for Migrations:**

```bash
# Initialize Alembic (one-time setup)
alembic init alembic

# Create a new migration
alembic revision -m "add_new_column_to_users"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

**Migration Example:**

```python
# alembic/versions/001_add_confidence_column.py
"""add confidence column to sessions table

Revision ID: 001
Created Date: 2025-10-05
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Apply changes"""
    op.add_column(
        'sessions',
        sa.Column('confidence', sa.Float, nullable=True)
    )

def downgrade():
    """Revert changes"""
    op.drop_column('sessions', 'confidence')
```

**Manual Migration (without Alembic):**

```python
# scripts/migrate_database.py
import sqlite3
from pathlib import Path

def migrate_add_confidence_column():
    """
    Migration: Add confidence column to sessions table
    """
    db_path = Path("database/vsl_app.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(sessions)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'confidence' not in columns:
            # Add column
            cursor.execute("""
                ALTER TABLE sessions
                ADD COLUMN confidence REAL
            """)
            conn.commit()
            print("✓ Added confidence column to sessions table")
        else:
            print("✓ Column already exists")

    except Exception as e:
        conn.rollback()
        print(f"✗ Migration failed: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_add_confidence_column()
```

### 8.2 Schema Changes / Thay đổi schema

**Rules:**
1. NEVER modify database directly in production
2. ALWAYS create migration script
3. ALWAYS test migration on copy of database first
4. ALWAYS have rollback plan
5. Backup database before migration

**Adding New Table:**

```python
# database/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class GestureTemplate(Base):
    """
    New table: gesture_templates

    Stores template gestures for recognition
    """
    __tablename__ = "gesture_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, index=True)
    keypoints = Column(String)  # JSON string
    vsl_vocab_id = Column(Integer, ForeignKey("vsl_vocabulary.id"))
    confidence_threshold = Column(Float, default=0.5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    vocabulary = relationship("VSLVocabulary", back_populates="gesture_templates")
```

**Migration Script:**

```python
# migrations/002_add_gesture_templates.py
def upgrade():
    op.create_table(
        'gesture_templates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String()),
        sa.Column('keypoints', sa.String()),
        sa.Column('vsl_vocab_id', sa.Integer()),
        sa.Column('confidence_threshold', sa.Float(), default=0.5),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.now),
        sa.Column('updated_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['vsl_vocab_id'], ['vsl_vocabulary.id'])
    )
    op.create_index('ix_gesture_templates_name', 'gesture_templates', ['name'])
    op.create_index('ix_gesture_templates_category', 'gesture_templates', ['category'])

def downgrade():
    op.drop_index('ix_gesture_templates_category')
    op.drop_index('ix_gesture_templates_name')
    op.drop_table('gesture_templates')
```

### 8.3 Query Optimization / Tối ưu hóa query

**Use Indexes:**

```python
# ✅ GOOD - Indexed columns for frequent queries
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Indexed
    session_type = Column(String, index=True)  # Indexed
    created_at = Column(DateTime, default=datetime.now, index=True)  # Indexed

# Fast query because columns are indexed
sessions = db.query(Session)\
    .filter(Session.user_id == user_id)\
    .filter(Session.session_type == "vsl_recognition")\
    .order_by(Session.created_at.desc())\
    .all()
```

**Use Pagination:**

```python
# ✅ GOOD - Paginated query
def get_sessions_paginated(db: Session, page: int = 1, page_size: int = 20):
    """
    Get sessions with pagination

    INPUT:
        db: Database session
        page: Page number (1-indexed)
        page_size: Items per page
    OUTPUT:
        {
            'items': list of sessions,
            'total': total count,
            'page': current page,
            'page_size': page size,
            'total_pages': total pages
        }
    """
    offset = (page - 1) * page_size

    # Get total count
    total = db.query(Session).count()

    # Get paginated items
    items = db.query(Session)\
        .offset(offset)\
        .limit(page_size)\
        .all()

    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

# ❌ BAD - Load all records (slow with large tables)
def get_all_sessions(db: Session):
    return db.query(Session).all()  # Could be millions of records!
```

**Use Joins Efficiently:**

```python
# ✅ GOOD - Join with select only needed columns
def get_sessions_with_user(db: Session):
    """Get sessions with user info"""
    return db.query(
        Session.id,
        Session.session_type,
        Session.created_at,
        User.username,
        User.email
    ).join(User, Session.user_id == User.id)\
     .all()

# ❌ BAD - N+1 query problem
def get_sessions_with_user_bad(db: Session):
    sessions = db.query(Session).all()
    for session in sessions:
        session.user = db.query(User).filter(User.id == session.user_id).first()
    # This executes N+1 queries (1 for sessions + N for users)
    return sessions

# ✅ GOOD - Use eager loading
def get_sessions_with_user_good(db: Session):
    return db.query(Session)\
        .options(joinedload(Session.user))\
        .all()
    # This executes only 1 query with JOIN
```

**Cache Frequent Queries:**

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache gesture templates (they don't change often)
@lru_cache(maxsize=1)
def get_gesture_templates_cached(db: Session):
    """
    Get all gesture templates (cached)
    Cache invalidates every 5 minutes
    """
    return db.query(GestureTemplate)\
        .filter(GestureTemplate.is_active == True)\
        .all()

# Clear cache when templates are updated
def update_gesture_template(db: Session, template_id: int, data: dict):
    template = db.query(GestureTemplate).get(template_id)
    for key, value in data.items():
        setattr(template, key, value)
    db.commit()

    # Clear cache
    get_gesture_templates_cached.cache_clear()
```

### 8.4 Database Best Practices / Best practices cho database

**1. Always Use Transactions:**

```python
from sqlalchemy.orm import Session

# ✅ GOOD - Use transaction
def create_session_with_results(db: Session, session_data: dict, results: list):
    """
    Create session and results in single transaction
    """
    try:
        # Start transaction (implicit)
        new_session = Session(**session_data)
        db.add(new_session)
        db.flush()  # Get new_session.id without committing

        for result_data in results:
            result = Result(session_id=new_session.id, **result_data)
            db.add(result)

        db.commit()  # Commit all changes together
        return new_session

    except Exception as e:
        db.rollback()  # Rollback on error
        logger.error(f"Error creating session: {str(e)}")
        raise
```

**2. Use Context Managers:**

```python
# ✅ GOOD - Auto-close database connection
from contextlib import contextmanager

@contextmanager
def get_db_context():
    """Database context manager"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Usage
with get_db_context() as db:
    user = db.query(User).first()
    # db is automatically committed and closed
```

**3. Validate Before Database Operations:**

```python
# ✅ GOOD - Validate before DB operation
def create_user(db: Session, user_data: dict):
    """
    Create new user with validation
    """
    # Validate
    if not user_data.get('username'):
        raise ValueError("Username is required")

    if not user_data.get('email'):
        raise ValueError("Email is required")

    # Check if user already exists
    existing = db.query(User)\
        .filter(User.username == user_data['username'])\
        .first()
    if existing:
        raise ValueError("Username already exists")

    # Create user
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

---

## 9. Frontend Development Rules
## Quy tắc phát triển Frontend

### 9.1 Component Structure / Cấu trúc component

**Component File Structure:**

```javascript
// CameraToText.jsx
import React, { useState, useEffect } from 'react'
import { Box, Button, Typography, CircularProgress } from '@mui/material'
import api from '../../services/api'
import { showNotification } from '../../utils/notifications'

/**
 * CameraToText Component
 *
 * Allows users to upload video/image for VSL recognition
 *
 * Features:
 * - Video file upload
 * - Real-time camera capture
 * - Display recognition results
 */
const CameraToText = () => {
  // ============ STATE ============
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // ============ EFFECTS ============
  useEffect(() => {
    // Cleanup on unmount
    return () => {
      // Cancel pending requests, cleanup resources
    }
  }, [])

  // ============ HANDLERS ============
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      // Validate file
      if (!validateFile(selectedFile)) {
        setError('Invalid file format')
        return
      }
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    try {
      setLoading(true)
      setError(null)

      const formData = new FormData()
      formData.append('file', file)

      const response = await api.post('/api/v1/vsl/recognize-video', formData)

      if (response.data.success) {
        setResult(response.data.data)
        showNotification('Processing completed', 'success')
      }
    } catch (err) {
      setError(err.message)
      showNotification('Upload failed', 'error')
    } finally {
      setLoading(false)
    }
  }

  // ============ HELPERS ============
  const validateFile = (file) => {
    const allowedTypes = ['video/mp4', 'video/avi', 'video/mov']
    const maxSize = 100 * 1024 * 1024 // 100MB

    if (!allowedTypes.includes(file.type)) {
      return false
    }
    if (file.size > maxSize) {
      return false
    }
    return true
  }

  // ============ RENDER ============
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        VSL Recognition from Camera/Video
      </Typography>

      {/* File Upload Section */}
      <Box sx={{ mb: 3 }}>
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="video-upload"
        />
        <label htmlFor="video-upload">
          <Button variant="contained" component="span">
            Choose Video
          </Button>
        </label>
        {file && <Typography>{file.name}</Typography>}
      </Box>

      {/* Upload Button */}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? <CircularProgress size={24} /> : 'Upload'}
      </Button>

      {/* Error Display */}
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      {/* Results Display */}
      {result && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Results:</Typography>
          <Typography>Detected: {result.detected_text}</Typography>
          <Typography>Confidence: {result.confidence.toFixed(2)}</Typography>
        </Box>
      )}
    </Box>
  )
}

export default CameraToText
```

**Component Structure Rules:**

1. **Order of sections:**
   - Imports
   - Component documentation (JSDoc)
   - State declarations
   - Effects (useEffect, etc.)
   - Event handlers
   - Helper functions
   - Render/return

2. **File size:** < 300 lines
   - If longer, split into sub-components

3. **One component per file**
   - Exception: Small helper components can be in same file

### 9.2 State Management / Quản lý state

**Local State (useState):**

```javascript
// Use for component-specific state
const [value, setValue] = useState(initialValue)
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)
```

**Global State (Context API):**

```javascript
// contexts/AppContext.jsx
import React, { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [settings, setSettings] = useState({
    language: 'vi',
    theme: 'light'
  })

  const value = {
    user,
    setUser,
    settings,
    setSettings
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

// Usage in component
import { useApp } from '../../contexts/AppContext'

function MyComponent() {
  const { user, settings, setSettings } = useApp()

  return <div>User: {user?.name}</div>
}
```

**When to use global vs local state:**

| Use Local State | Use Global State |
|----------------|------------------|
| Form inputs | User authentication |
| UI toggles (modals, dropdowns) | App settings |
| Component-specific data | Theme preferences |
| Temporary data | Language selection |
| Loading/error states | Shared data across routes |

### 9.3 API Integration Patterns / Mẫu tích hợp API

**API Service Layer:**

```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// services/vslService.js - Specific API functions
export const vslService = {
  /**
   * Recognize VSL from video
   */
  recognizeVideo: async (file, options = {}) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/v1/vsl/recognize-video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      params: options
    })
    return response.data
  },

  /**
   * Recognize VSL from image
   */
  recognizeImage: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/v1/vsl/recognize-image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  /**
   * Get list of gestures
   */
  getGestures: async () => {
    const response = await api.get('/api/v1/vsl/gestures')
    return response.data
  }
}
```

**Using API in Components:**

```javascript
import { useState } from 'react'
import { vslService } from '../../services/vslService'

function CameraToText() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleVideoUpload = async (file) => {
    try {
      setLoading(true)
      setError(null)

      const data = await vslService.recognizeVideo(file, {
        confidence_threshold: 0.7,
        max_frames: 500
      })

      if (data.success) {
        setResult(data.data)
      } else {
        throw new Error(data.error || 'Processing failed')
      }

    } catch (err) {
      console.error('Error uploading video:', err)
      setError(err.response?.data?.error || err.message)

    } finally {
      setLoading(false)
    }
  }

  return (
    // Component JSX
  )
}
```

**Custom Hooks for API:**

```javascript
// hooks/useVideoRecognition.js
import { useState, useCallback } from 'react'
import { vslService } from '../services/vslService'

export const useVideoRecognition = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const recognizeVideo = useCallback(async (file, options) => {
    try {
      setLoading(true)
      setError(null)

      const data = await vslService.recognizeVideo(file, options)

      if (data.success) {
        setResult(data.data)
        return data.data
      } else {
        throw new Error(data.error)
      }

    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message
      setError(errorMessage)
      throw err

    } finally {
      setLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  return {
    loading,
    result,
    error,
    recognizeVideo,
    reset
  }
}

// Usage in component
function CameraToText() {
  const { loading, result, error, recognizeVideo } = useVideoRecognition()

  const handleUpload = async (file) => {
    try {
      await recognizeVideo(file, { confidence_threshold: 0.7 })
      // Handle success
    } catch (err) {
      // Error already set in hook
    }
  }

  return (
    // Component JSX
  )
}
```

### 9.4 UI/UX Guidelines / Hướng dẫn UI/UX

**Loading States:**

```javascript
// ✅ GOOD - Show loading indicator
{loading && <CircularProgress />}
{loading ? 'Processing...' : 'Upload'}

// Show skeleton while loading
{loading ? (
  <Skeleton variant="rectangular" width={300} height={200} />
) : (
  <ResultsDisplay data={result} />
)}
```

**Error Handling:**

```javascript
// ✅ GOOD - User-friendly error messages
{error && (
  <Alert severity="error" sx={{ mt: 2 }}>
    {error}
  </Alert>
)}

// Specific error messages
const getErrorMessage = (error) => {
  if (error.response?.status === 413) {
    return 'File size too large. Maximum 100MB allowed.'
  }
  if (error.response?.status === 400) {
    return error.response.data.error || 'Invalid file format'
  }
  if (error.response?.status >= 500) {
    return 'Server error. Please try again later.'
  }
  return error.message || 'An error occurred'
}
```

**Responsive Design:**

```javascript
// Use Material-UI breakpoints
<Box
  sx={{
    width: { xs: '100%', sm: '80%', md: '60%' },
    p: { xs: 2, sm: 3, md: 4 }
  }}
>
  Content
</Box>

// Mobile-first approach
sx={{
  flexDirection: { xs: 'column', md: 'row' },
  gap: { xs: 2, md: 3 }
}}
```

**Accessibility:**

```javascript
// ✅ GOOD - Accessible button
<Button
  variant="contained"
  onClick={handleClick}
  aria-label="Upload video for VSL recognition"
  disabled={loading}
>
  Upload Video
</Button>

// Accessible form inputs
<TextField
  label="Enter text"
  value={text}
  onChange={handleChange}
  aria-describedby="text-helper"
  helperText={<span id="text-helper">Enter Vietnamese text</span>}
/>
```

---

## 10. Code Quality
## Chất lượng code

### 10.1 Linting Rules / Quy tắc linting

**Backend (Python) - Flake8:**

```ini
# .flake8
[flake8]
max-line-length = 100
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    alembic
ignore =
    E203,  # whitespace before ':'
    W503,  # line break before binary operator
per-file-ignores =
    __init__.py:F401  # Allow unused imports in __init__.py
```

**Run linter:**
```bash
# Check code
flake8 .

# Auto-fix some issues with black
black .

# Check imports
isort .
```

**Frontend (JavaScript) - ESLint:**

```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 12,
    sourceType: 'module'
  },
  plugins: ['react'],
  rules: {
    'react/react-in-jsx-scope': 'off',  // Not needed in React 17+
    'react/prop-types': 'warn',
    'no-unused-vars': 'warn',
    'no-console': 'warn',
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'never']
  },
  settings: {
    react: {
      version: 'detect'
    }
  }
}
```

**Run linter:**
```bash
# Check code
npm run lint

# Auto-fix
npm run lint:fix
```

### 10.2 Formatting Standards / Chuẩn format code

**Python - Black:**

```python
# ✅ GOOD - Black formatted
def calculate_similarity(
    landmarks1: list,
    landmarks2: list,
    threshold: float = 0.5
) -> float:
    """Calculate similarity"""
    if not landmarks1 or not landmarks2:
        return 0.0

    # Calculate features
    features1 = extract_features(landmarks1)
    features2 = extract_features(landmarks2)

    # Compute similarity
    similarity = cosine_similarity(features1, features2)

    return similarity if similarity >= threshold else 0.0
```

**JavaScript - Prettier:**

```javascript
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 80,
  "arrowParens": "always"
}

// ✅ GOOD - Prettier formatted
const calculateSimilarity = (landmarks1, landmarks2, threshold = 0.5) => {
  if (!landmarks1 || !landmarks2) {
    return 0.0
  }

  const features1 = extractFeatures(landmarks1)
  const features2 = extractFeatures(landmarks2)
  const similarity = cosineSimilarity(features1, features2)

  return similarity >= threshold ? similarity : 0.0
}
```

### 10.3 Performance Guidelines / Hướng dẫn hiệu năng

**Backend Performance:**

```python
# ✅ GOOD - Efficient processing
def process_large_video(video_path: str):
    """
    Process large video efficiently using generators
    """
    # Use generator to avoid loading all frames into memory
    def frame_generator():
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
        cap.release()

    results = []
    for frame in frame_generator():
        result = process_frame(frame)
        results.append(result)

    return results

# ❌ BAD - Load all frames at once (memory intensive)
def process_large_video_bad(video_path: str):
    frames = []
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)  # Loads all into memory!
    cap.release()

    return [process_frame(f) for f in frames]
```

**Frontend Performance:**

```javascript
// ✅ GOOD - Memoize expensive calculations
import { useMemo, useCallback } from 'react'

function ResultsDisplay({ data }) {
  // Memoize expensive calculation
  const processedData = useMemo(() => {
    return expensiveDataProcessing(data)
  }, [data])

  // Memoize callback
  const handleClick = useCallback(() => {
    doSomething(data)
  }, [data])

  return <div>{processedData}</div>
}

// ✅ GOOD - Lazy load components
import { lazy, Suspense } from 'react'

const HeavyComponent = lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  )
}

// ✅ GOOD - Debounce user input
import { useState, useEffect } from 'react'

function SearchBox() {
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query)
    }, 500)  // Wait 500ms after user stops typing

    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    if (debouncedQuery) {
      // Perform search with debounced query
      performSearch(debouncedQuery)
    }
  }, [debouncedQuery])

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />
}
```

### 10.4 Security Best Practices / Best practices về bảo mật

**Backend Security:**

```python
# ✅ GOOD - Validate and sanitize inputs
from pathlib import Path
import re

def validate_filename(filename: str) -> bool:
    """
    Validate filename to prevent path traversal attacks
    """
    # Remove any directory path
    filename = Path(filename).name

    # Check for dangerous patterns
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # Allow only alphanumeric, dash, underscore, dot
    if not re.match(r'^[\w\-. ]+$', filename):
        return False

    return True

# ✅ GOOD - Don't expose internal errors
try:
    result = process_data(data)
except Exception as e:
    logger.error(f"Internal error: {str(e)}", exc_info=True)

    if settings.DEBUG:
        # Show detailed error in development
        raise
    else:
        # Generic error in production
        return create_response(
            success=False,
            error="An error occurred while processing your request"
        )

# ✅ GOOD - Use environment variables for secrets
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Never hardcode!
DATABASE_URL = os.getenv('DATABASE_URL')

# ❌ BAD - Hardcoded secrets
API_KEY = "abc123secret"  # DON'T DO THIS!
```

**Frontend Security:**

```javascript
// ✅ GOOD - Sanitize user input before rendering
import DOMPurify from 'dompurify'

function DisplayUserContent({ content }) {
  // Sanitize HTML to prevent XSS
  const cleanContent = DOMPurify.sanitize(content)

  return <div dangerouslySetInnerHTML={{ __html: cleanContent }} />
}

// ✅ GOOD - Store tokens securely
// Use httpOnly cookies (set by backend) instead of localStorage for sensitive tokens

// If you must use localStorage, encrypt sensitive data
import CryptoJS from 'crypto-js'

const encryptData = (data, secretKey) => {
  return CryptoJS.AES.encrypt(JSON.stringify(data), secretKey).toString()
}

const decryptData = (encryptedData, secretKey) => {
  const bytes = CryptoJS.AES.decrypt(encryptedData, secretKey)
  return JSON.parse(bytes.toString(CryptoJS.enc.Utf8))
}

// ✅ GOOD - Use environment variables
// .env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=VSL Application

// Access in code
const apiUrl = import.meta.env.VITE_API_URL

// ❌ BAD - Expose API keys in frontend code
const API_KEY = "secret_key"  // DON'T DO THIS!
```

---

## Quick Reference / Tham khảo nhanh

### Common Commands / Lệnh thường dùng

**Backend:**
```bash
# Run server
python -m uvicorn app.main:app --reload

# Run tests
pytest
pytest --cov=app

# Format code
black .
isort .

# Lint
flake8 .

# Database migration
alembic upgrade head
alembic revision -m "description"
```

**Frontend:**
```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint
npm run lint
npm run lint:fix

# Format
npm run format
```

**Git:**
```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit
git add .
git commit -m "feat(module): description"

# Push
git push origin feature/my-feature

# Update branch
git checkout main
git pull
git checkout feature/my-feature
git merge main
```

### Checklist Before Commit / Kiểm tra trước khi commit

- [ ] Code đã được test
- [ ] Tất cả tests pass
- [ ] Code đã được format (black/prettier)
- [ ] Code đã được lint (flake8/eslint)
- [ ] Không có files > 800 lines
- [ ] Tất cả functions có docstring
- [ ] Không có console.log/print debug statements
- [ ] Không có hardcoded secrets
- [ ] Error handling đầy đủ
- [ ] Input validation đầy đủ

### Checklist Before PR / Kiểm tra trước khi tạo PR

- [ ] Branch updated với main
- [ ] Không có merge conflicts
- [ ] Tất cả tests pass
- [ ] Code review checklist đã check
- [ ] Documentation updated (nếu cần)
- [ ] PR description đầy đủ
- [ ] Screenshots added (nếu có UI changes)

---

## Resources / Tài nguyên

### Documentation
- **FastAPI:** https://fastapi.tiangolo.com
- **React:** https://react.dev
- **Material-UI:** https://mui.com
- **SQLAlchemy:** https://docs.sqlalchemy.org
- **MediaPipe:** https://developers.google.com/mediapipe

### Tools
- **Python Formatter:** Black (https://github.com/psf/black)
- **Python Linter:** Flake8 (https://flake8.pycqa.org)
- **JS Formatter:** Prettier (https://prettier.io)
- **JS Linter:** ESLint (https://eslint.org)

---

## Contact / Liên hệ

Nếu có thắc mắc về Development Rules, liên hệ:
- Team Lead
- Project Mentor
- Create issue trên GitHub repository

---

**END OF DOCUMENT**

**Version:** 1.0.0
**Last Updated:** 2025-10-05
