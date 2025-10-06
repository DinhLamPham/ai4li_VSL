"""
Database Connection Management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from ..config import settings

# Create SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency để lấy database session

    INPUT: None
    OUTPUT: Generator[Session]
    USAGE:
        from fastapi import Depends
        from app.database.db import get_db

        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Khởi tạo database - tạo tất cả tables và seed initial data

    INPUT: None
    OUTPUT: None
    SIDE EFFECTS:
        - Tạo tables trong database
        - Tạo admin user nếu chưa tồn tại
    USAGE:
        from app.database.db import init_db
        init_db()  # Tạo tất cả tables và seed data
    """
    import logging
    from .models import User, VSLVocabulary, GestureTemplate, Session as SessionModel, ModelRegistry, TrainingData

    logger = logging.getLogger(__name__)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == 'admin').first()

        if not admin_user:
            # Create default admin user
            admin_user = User(
                username='admin',
                password='123456',  # POC: plain text password
                email='admin@vsl.app',
                full_name='System Administrator',
                role='admin',
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Created default admin user (admin/123456)")
        else:
            logger.info("Admin user already exists")

    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()
