"""
VSL Gloss Annotation Tool - Group 3

STUDENT TODO: Implement gloss annotation tool
"""
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


def create_annotation(video_path: str, gloss: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Tạo annotation cho video với gloss

    INPUT:
        video_path: str - Path to video
        gloss: str - VSL gloss notation
        metadata: dict - Additional metadata

    OUTPUT:
        {
            'success': bool,
            'annotation_id': int,
            'video_path': str,
            'gloss': str,
            'created_at': str
        }

    STUDENT TODO:
        1. Validate video và gloss
        2. Save annotation to database
        3. Return annotation info
    """
    # PLACEHOLDER
    print("[GLOSS_TOOL] create_annotation called")

    # TODO: Save to database
    return {
        'success': True,
        'annotation_id': 0,
        'video_path': video_path,
        'gloss': gloss,
        'created_at': ""
    }


def get_annotations(filters: Optional[Dict] = None) -> List[Dict]:
    """
    Lấy danh sách annotations

    INPUT:
        filters: dict - Filter options:
            - category: str
            - date_from: str
            - date_to: str

    OUTPUT:
        List of annotation dicts

    STUDENT TODO:
        - Query database với filters
        - Return results
    """
    # PLACEHOLDER
    print("[GLOSS_TOOL] get_annotations called")

    # TODO: Query database
    return []


def validate_gloss(gloss: str) -> Dict[str, Any]:
    """
    Validate gloss notation

    INPUT:
        gloss: str - VSL gloss

    OUTPUT:
        {
            'valid': bool,
            'errors': list,
            'warnings': list
        }

    STUDENT TODO:
        - Check gloss format
        - Check against vocabulary
        - Check grammar markers
        - Return validation results
    """
    # PLACEHOLDER
    print("[GLOSS_TOOL] validate_gloss called")

    return {
        'valid': True,
        'errors': [],
        'warnings': []
    }
