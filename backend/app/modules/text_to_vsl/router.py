"""
Text to VSL Router - API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ...database.db import get_db
from ...database.schemas import TextToVSLRequest, APIResponse
from ...core.utils import create_response
from . import translation_service, avatar_3d, gloss_tool

router = APIRouter(prefix="/vsl", tags=["Text to VSL"])


@router.post("/text-to-vsl", response_model=APIResponse)
async def text_to_vsl_endpoint(
    request: TextToVSLRequest,
    db: Session = Depends(get_db)
):
    """
    Chuyển text thành VSL gloss

    **INPUT:**
    - text: Vietnamese text
    - options: Translation options

    **OUTPUT:**
    - VSL gloss notation
    - Vocabulary matches
    """
    try:
        result = translation_service.text_to_vsl(request.text, request.options)

        return create_response(
            success=result['success'],
            message="Translation completed",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Translation failed",
            error=str(e)
        )


@router.post("/generate-avatar", response_model=APIResponse)
async def generate_avatar_endpoint(
    request: TextToVSLRequest,
    db: Session = Depends(get_db)
):
    """
    Generate 3D avatar animation từ text

    **INPUT:**
    - text: Vietnamese text

    **OUTPUT:**
    - Animation URL/path
    """
    try:
        # First convert to gloss
        translation_result = translation_service.text_to_vsl(request.text)

        if not translation_result['success']:
            return create_response(
                success=False,
                message="Translation failed",
                error=translation_result.get('error')
            )

        # Generate animation
        animation_result = avatar_3d.generate_avatar_animation(
            translation_result['gloss'],
            request.options
        )

        return create_response(
            success=animation_result['success'],
            message="Animation generated",
            data={
                **translation_result,
                **animation_result
            }
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Animation generation failed",
            error=str(e)
        )


@router.get("/vocabulary", response_model=APIResponse)
async def get_vocabulary(db: Session = Depends(get_db)):
    """
    Lấy danh sách VSL vocabulary
    """
    # PLACEHOLDER
    print("[API] GET /vsl/vocabulary called")

    # TODO: Query database
    return create_response(
        success=True,
        message="Vocabulary retrieved",
        data={'vocabulary': []}
    )


@router.post("/gloss-tool/annotate", response_model=APIResponse)
async def create_annotation_endpoint(
    video_path: str,
    gloss: str,
    db: Session = Depends(get_db)
):
    """
    Create gloss annotation

    **STUDENT TODO:**
    - Validate inputs
    - Call gloss_tool.create_annotation()
    """
    try:
        result = gloss_tool.create_annotation(video_path, gloss)

        return create_response(
            success=result['success'],
            message="Annotation created",
            data=result
        )

    except Exception as e:
        return create_response(
            success=False,
            message="Annotation failed",
            error=str(e)
        )
