"""
Application Configuration
Quản lý cấu hình cho toàn bộ ứng dụng VSL
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Cấu hình chung cho ứng dụng

    Các biến môi trường có thể được đặt trong file .env hoặc environment variables
    """
    # Application
    APP_NAME: str = "VSL Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./database/vsl_app.db"

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASE_DIR: Path = BASE_DIR / "database"

    # Model paths
    VSL_RECOGNITION_MODEL_DIR: Path = MODELS_DIR / "vsl_recognition"
    GESTURE_MODEL_DIR: Path = MODELS_DIR / "gesture"
    EMOTION_MODEL_DIR: Path = MODELS_DIR / "emotion"

    # Data paths
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    AUGMENTED_DATA_DIR: Path = DATA_DIR / "augmented"

    # Upload settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".avi", ".mov", ".mkv"}
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".bmp"}
    ALLOWED_AUDIO_EXTENSIONS: set = {".wav", ".mp3", ".ogg", ".flac"}

    # MediaPipe settings
    MEDIAPIPE_MIN_DETECTION_CONFIDENCE: float = 0.5
    MEDIAPIPE_MIN_TRACKING_CONFIDENCE: float = 0.5

    # Processing settings
    MAX_WORKERS: int = 4
    PROCESSING_TIMEOUT: int = 300  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def create_directories(self):
        """
        Tạo các thư mục cần thiết nếu chưa tồn tại

        INPUT: None
        OUTPUT: None
        SIDE EFFECTS: Tạo các thư mục trên hệ thống file
        """
        directories = [
            self.MODELS_DIR,
            self.VSL_RECOGNITION_MODEL_DIR,
            self.GESTURE_MODEL_DIR,
            self.EMOTION_MODEL_DIR,
            self.DATA_DIR,
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.AUGMENTED_DATA_DIR,
            self.DATABASE_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Create necessary directories on import
settings.create_directories()
