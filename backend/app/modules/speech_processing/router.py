"""
Speech Processing Router - API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ...database.db import get_db
from ...database.schemas import AudioToTextResponse, TextToAudioRequest, APIResponse
from ...config import settings
from ...core.utils import save_uploaded_file, validate_file_extension, create_response
from . import stt_service, tts_service

router = APIRouter(prefix="/speech", tags=["Speech Processing"])


@router.post("/audio-to-text", response_model=APIResponse)
async def audio_to_text_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Speech-to-Text: Chuyển audio thành text

    **INPUT:**
    - file: Audio file (wav, mp3, ogg, flac)

    **OUTPUT:**
    - Transcribed text with confidence

    **STUDENT TODO:**
    - Validate file
    - Save file
    - Call stt_service.audio_to_text()
    - Return results
    """
    try:
        # Validate
        if not validate_file_extension(file.filename, settings.ALLOWED_AUDIO_EXTENSIONS):
            return create_response(
                success=False,
                message="Invalid file extension",
                error="Allowed: wav, mp3, ogg, flac"
            )

        # Save file
        file_content = await file.read()
        file_path = save_uploaded_file(
            file_content,
            file.filename,
            settings.RAW_DATA_DIR / "audio"
        )

        # Call STT service
        result = stt_service.audio_to_text(file_path)

        return create_response(
            success=result['success'],
            message="Audio processed" if result['success'] else "Processing failed",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Error processing audio",
            error=str(e)
        )


@router.post("/text-to-audio", response_model=APIResponse)
async def text_to_audio_endpoint(
    request: TextToAudioRequest,
    db: Session = Depends(get_db)
):
    """
    Text-to-Speech: Chuyển text thành audio

    **INPUT:**
    - text: Text cần chuyển đổi
    - voice: Voice ID (optional)
    - language: Ngôn ngữ (default: 'vi')

    **OUTPUT:**
    - Audio file path/URL

    **STUDENT TODO:**
    - Validate text
    - Call tts_service.text_to_audio()
    - Return audio file
    """
    try:
        # Call TTS service
        options = {
            'voice': request.voice,
            'language': request.language
        }

        result = tts_service.text_to_audio(request.text, options)

        return create_response(
            success=result['success'],
            message="Audio generated" if result['success'] else "Generation failed",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Error generating audio",
            error=str(e)
        )


@router.get("/voices", response_model=APIResponse)
async def get_voices():
    """
    Lấy danh sách voices có sẵn

    **OUTPUT:**
    - List of available voices
    """
    voices = tts_service.get_available_voices()
    return create_response(
        success=True,
        message="Voices retrieved",
        data={'voices': voices}
    )


@router.get("/status", response_model=APIResponse)
async def get_status():
    """
    Check processing status

    **STUDENT TODO:**
    - Implement status tracking cho async processing
    """
    # PLACEHOLDER
    print("[API] GET /speech/status called")

    return create_response(
        success=True,
        message="Status retrieved",
        data={'status': 'ready'}
    )
