"""
Pydantic Schemas - Request/Response validation

Schemas cho API validation và serialization
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base User schema"""
    username: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = Field(default='user', pattern='^(admin|user|student)$')


class UserCreate(UserBase):
    """Schema để tạo user mới"""
    password: str = Field(..., min_length=3)  # POC: plain text, min 3 chars


class UserResponse(UserBase):
    """Schema cho response User"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# VSL Vocabulary Schemas
class VSLVocabularyBase(BaseModel):
    """Base VSL Vocabulary schema"""
    word_vn: str
    word_en: Optional[str] = None
    gloss: Optional[str] = None
    category: Optional[str] = None
    video_path: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None


class VSLVocabularyCreate(VSLVocabularyBase):
    """Schema để tạo VSL vocabulary mới"""
    pass


class VSLVocabularyResponse(VSLVocabularyBase):
    """Schema cho response VSL Vocabulary"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Gesture Template Schemas
class GestureTemplateBase(BaseModel):
    """Base Gesture Template schema"""
    name: str
    keypoints: str  # JSON string
    vsl_vocab_id: Optional[int] = None


class GestureTemplateCreate(GestureTemplateBase):
    """Schema để tạo gesture template mới"""
    pass


class GestureTemplateResponse(GestureTemplateBase):
    """Schema cho response Gesture Template"""
    id: int

    class Config:
        from_attributes = True


# Session Schemas
class SessionBase(BaseModel):
    """Base Session schema"""
    user_id: Optional[int] = None
    session_type: str
    input_data: Optional[str] = None  # JSON string
    output_data: Optional[str] = None  # JSON string


class SessionCreate(SessionBase):
    """Schema để tạo session mới"""
    pass


class SessionResponse(SessionBase):
    """Schema cho response Session"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Model Registry Schemas
class ModelRegistryBase(BaseModel):
    """Base Model Registry schema"""
    model_name: str
    model_version: Optional[str] = None
    model_type: str
    model_path: str
    metrics: Optional[str] = None  # JSON string
    is_active: bool = False


class ModelRegistryCreate(ModelRegistryBase):
    """Schema để tạo model registry entry mới"""
    pass


class ModelRegistryResponse(ModelRegistryBase):
    """Schema cho response Model Registry"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Training Data Schemas
class TrainingDataBase(BaseModel):
    """Base Training Data schema"""
    data_type: str
    file_path: str
    label: Optional[str] = None
    is_augmented: bool = False
    source_id: Optional[int] = None


class TrainingDataCreate(TrainingDataBase):
    """Schema để tạo training data entry mới"""
    pass


class TrainingDataResponse(TrainingDataBase):
    """Schema cho response Training Data"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# API Response Schemas
class APIResponse(BaseModel):
    """
    Standardized API Response

    USAGE:
        return APIResponse(
            success=True,
            message="Operation completed",
            data={"result": "value"}
        )
    """
    success: bool
    message: str = ""
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# VSL Recognition Schemas
class VSLRecognitionRequest(BaseModel):
    """
    Request schema cho VSL recognition

    INPUT:
        file: Upload file (video/image) - handled by FastAPI UploadFile
        options: Dict chứa các options
    """
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class VSLRecognitionResponse(BaseModel):
    """
    Response schema cho VSL recognition

    OUTPUT:
        success: bool
        detected_text: Text được nhận diện
        confidence: Độ tin cậy
        landmarks: Landmarks data (optional)
        processing_time: Thời gian xử lý (seconds)
    """
    success: bool
    detected_text: Optional[str] = None
    confidence: Optional[float] = None
    landmarks: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None


# Speech Processing Schemas
class AudioToTextRequest(BaseModel):
    """Request schema cho Audio to Text"""
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AudioToTextResponse(BaseModel):
    """
    Response schema cho Audio to Text

    OUTPUT:
        success: bool
        text: Text được chuyển đổi
        confidence: Độ tin cậy
        language: Ngôn ngữ phát hiện
        processing_time: Thời gian xử lý
    """
    success: bool
    text: Optional[str] = None
    confidence: Optional[float] = None
    language: Optional[str] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None


class TextToAudioRequest(BaseModel):
    """
    Request schema cho Text to Audio

    INPUT:
        text: Text cần chuyển đổi
        voice: Voice ID (optional)
        language: Ngôn ngữ (default: 'vi')
    """
    text: str
    voice: Optional[str] = None
    language: str = "vi"


class TextToAudioResponse(BaseModel):
    """
    Response schema cho Text to Audio

    OUTPUT:
        success: bool
        audio_url: URL hoặc path đến audio file
        duration: Thời lượng audio (seconds)
    """
    success: bool
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    error: Optional[str] = None


# Text to VSL Schemas
class TextToVSLRequest(BaseModel):
    """
    Request schema cho Text to VSL

    INPUT:
        text: Text tiếng Việt cần chuyển đổi
        options: Các options (speed, avatar_type, etc.)
    """
    text: str
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TextToVSLResponse(BaseModel):
    """
    Response schema cho Text to VSL

    OUTPUT:
        success: bool
        gloss: VSL gloss notation
        animation_url: URL đến 3D animation
        vocabulary_matches: Các từ matching trong vocabulary
    """
    success: bool
    gloss: Optional[str] = None
    animation_url: Optional[str] = None
    vocabulary_matches: Optional[list] = None
    error: Optional[str] = None
