"""
Database Models - SQLAlchemy ORM Models
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base


class User(Base):
    """
    User model - Quản lý người dùng

    Columns:
        id: Primary key
        username: Tên đăng nhập (unique)
        email: Email
        password: Mật khẩu (POC: plain text)
        full_name: Họ tên đầy đủ
        role: Vai trò (admin, user, student)
        is_active: Trạng thái hoạt động
        created_at: Thời gian tạo
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(255), nullable=False)  # POC: plain text
    full_name = Column(String(255))
    role = Column(String(50), default='user')  # admin, user, student
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="user")


class VSLVocabulary(Base):
    """
    VSL Vocabulary model - Từ vựng VSL

    Columns:
        id: Primary key
        word_vn: Từ tiếng Việt
        word_en: Từ tiếng Anh
        gloss: VSL gloss notation
        category: Danh mục (greeting, emotion, number, etc.)
        video_path: Đường dẫn video demo
        image_path: Đường dẫn hình ảnh
        description: Mô tả
        created_at: Thời gian tạo
    """
    __tablename__ = "vsl_vocabulary"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word_vn = Column(String(255), nullable=False, index=True)
    word_en = Column(String(255))
    gloss = Column(Text)
    category = Column(String(100), index=True)
    video_path = Column(Text)
    image_path = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    gesture_templates = relationship("GestureTemplate", back_populates="vsl_vocab")


class GestureTemplate(Base):
    """
    Gesture Template model - Template cho gesture recognition

    Columns:
        id: Primary key
        name: Tên gesture
        keypoints: JSON string chứa keypoints data
        vsl_vocab_id: Foreign key tới VSL vocabulary
    """
    __tablename__ = "gesture_templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    keypoints = Column(Text)  # JSON string
    vsl_vocab_id = Column(Integer, ForeignKey("vsl_vocabulary.id"))

    # Relationships
    vsl_vocab = relationship("VSLVocabulary", back_populates="gesture_templates")


class Session(Base):
    """
    Session model - Lưu lịch sử sử dụng

    Columns:
        id: Primary key
        user_id: Foreign key to users
        session_type: Loại session ('vsl_recognition', 'audio_to_text', etc.)
        input_data: Dữ liệu đầu vào (JSON string)
        output_data: Kết quả đầu ra (JSON string)
        created_at: Thời gian tạo
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_type = Column(String(100), index=True)
    input_data = Column(Text)  # JSON string
    output_data = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")


class ModelRegistry(Base):
    """
    Model Registry - Quản lý trained models

    Columns:
        id: Primary key
        model_name: Tên model
        model_version: Version của model
        model_type: Loại model ('vsl_recognition', 'gesture', 'emotion', etc.)
        model_path: Đường dẫn đến model file
        metrics: JSON string chứa metrics (accuracy, f1, etc.)
        is_active: Model có đang active không
        created_at: Thời gian tạo
    """
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(255), nullable=False, index=True)
    model_version = Column(String(100))
    model_type = Column(String(100), index=True)
    model_path = Column(Text)
    metrics = Column(Text)  # JSON string
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TrainingData(Base):
    """
    Training Data model - Quản lý training data

    Columns:
        id: Primary key
        data_type: Loại dữ liệu ('video', 'image', 'audio')
        file_path: Đường dẫn file
        label: Nhãn của data
        is_augmented: Có phải augmented data không
        source_id: ID của data gốc (nếu là augmented)
        created_at: Thời gian tạo
    """
    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_type = Column(String(50), index=True)
    file_path = Column(Text, nullable=False)
    label = Column(String(255), index=True)
    is_augmented = Column(Boolean, default=False)
    source_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
