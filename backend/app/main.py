"""
FastAPI Main Application
VSL Application Backend

Ứng dụng AI hỗ trợ người khiếm thính giao tiếp qua ngôn ngữ VSL
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import time
from pathlib import Path

from .config import settings
from .database.db import init_db, engine
from .database import models

# Import routers
from .modules.vsl_recognition.router import router as vsl_recognition_router
from .modules.speech_processing.router import router as speech_router
from .modules.text_to_vsl.router import router as text_to_vsl_router
from .modules.data_tools.router import router as data_tools_router
from .modules.user_management.router import router as user_management_router

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API Backend cho ứng dụng VSL - Hỗ trợ giao tiếp ngôn ngữ ký hiệu Việt Nam",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests và response time
    """
    start_time = time.time()

    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"Completed in {process_time:.3f}s - Status: {response.status_code}")

    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize database và các resources khi startup
    """
    logger.info("Starting VSL Application Backend...")

    # Initialize database
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")

    # Create necessary directories
    settings.create_directories()
    logger.info("Directories created")

    logger.info("Application startup complete!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup resources khi shutdown
    """
    logger.info("Shutting down VSL Application Backend...")

    # Release models
    from .core.model_manager import model_manager
    model_manager.release_models()

    logger.info("Application shutdown complete")


# Include routers
app.include_router(
    vsl_recognition_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    speech_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    text_to_vsl_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    data_tools_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    user_management_router,
    prefix=settings.API_V1_PREFIX
)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API info
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "api_prefix": settings.API_V1_PREFIX
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


# API Info endpoint
@app.get(f"{settings.API_V1_PREFIX}/info")
async def api_info():
    """
    API information endpoint
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_version": "v1",
        "endpoints": {
            "vsl_recognition": f"{settings.API_V1_PREFIX}/vsl",
            "speech_processing": f"{settings.API_V1_PREFIX}/speech",
            "text_to_vsl": f"{settings.API_V1_PREFIX}/vsl",
            "data_tools": f"{settings.API_V1_PREFIX}/tools"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
