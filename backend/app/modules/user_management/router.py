"""
User Management Router - API Endpoints
CRUD operations for user management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ...database.db import get_db
from ...database.models import User
from ...database.schemas import UserCreate, UserResponse, APIResponse
from ...core.utils import create_response

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("", response_model=APIResponse)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    include_disabled: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all users

    INPUT:
        - skip: int - Pagination offset
        - limit: int - Max results
        - include_disabled: bool - Include disabled users

    OUTPUT:
        {
            'success': bool,
            'data': {
                'users': [UserResponse, ...],
                'total': int
            }
        }
    """
    try:
        query = db.query(User)

        if not include_disabled:
            query = query.filter(User.is_active == True)

        total = query.count()
        users = query.offset(skip).limit(limit).all()

        return create_response(
            success=True,
            message=f"Retrieved {len(users)} users",
            data={
                'users': users,
                'total': total
            }
        )
    except Exception as e:
        return create_response(
            success=False,
            message="Failed to retrieve users",
            error=str(e)
        )


@router.get("/{user_id}", response_model=APIResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID

    INPUT:
        user_id: int - User ID

    OUTPUT:
        {
            'success': bool,
            'data': UserResponse
        }
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return create_response(
                success=False,
                message=f"User {user_id} not found",
                error="User not found"
            )

        return create_response(
            success=True,
            message="User retrieved",
            data={'user': user}
        )
    except Exception as e:
        return create_response(
            success=False,
            message="Failed to retrieve user",
            error=str(e)
        )


@router.post("", response_model=APIResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create new user

    INPUT:
        {
            'username': str,
            'email': str (optional),
            'password': str,
            'full_name': str (optional),
            'role': str (optional, default: 'user')
        }

    OUTPUT:
        {
            'success': bool,
            'data': {
                'user': UserResponse,
                'message': str
            }
        }
    """
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            return create_response(
                success=False,
                message="Username already exists",
                error="Duplicate username"
            )

        # Check if email already exists (if provided)
        if user_data.email:
            existing_email = db.query(User).filter(User.email == user_data.email).first()
            if existing_email:
                return create_response(
                    success=False,
                    message="Email already exists",
                    error="Duplicate email"
                )

        # Create new user
        # NOTE: In production, hash the password! This is POC only.
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,  # POC: storing plain text
            full_name=user_data.full_name,
            role=user_data.role or 'user',
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return create_response(
            success=True,
            message=f"User '{user_data.username}' created successfully",
            data={'user': new_user}
        )
    except Exception as e:
        db.rollback()
        return create_response(
            success=False,
            message="Failed to create user",
            error=str(e)
        )


@router.put("/{user_id}", response_model=APIResponse)
async def update_user(
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    full_name: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Update user

    INPUT:
        user_id: int - User ID
        username: str (optional)
        email: str (optional)
        password: str (optional)
        full_name: str (optional)
        role: str (optional)

    OUTPUT:
        {
            'success': bool,
            'data': UserResponse
        }
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return create_response(
                success=False,
                message=f"User {user_id} not found",
                error="User not found"
            )

        # Update fields if provided
        if username:
            # Check for duplicate username
            existing = db.query(User).filter(
                User.username == username,
                User.id != user_id
            ).first()
            if existing:
                return create_response(
                    success=False,
                    message="Username already exists",
                    error="Duplicate username"
                )
            user.username = username

        if email:
            # Check for duplicate email
            existing = db.query(User).filter(
                User.email == email,
                User.id != user_id
            ).first()
            if existing:
                return create_response(
                    success=False,
                    message="Email already exists",
                    error="Duplicate email"
                )
            user.email = email

        if password:
            user.password = password  # POC: plain text

        if full_name:
            user.full_name = full_name

        if role:
            user.role = role

        db.commit()
        db.refresh(user)

        return create_response(
            success=True,
            message=f"User '{user.username}' updated successfully",
            data={'user': user}
        )
    except Exception as e:
        db.rollback()
        return create_response(
            success=False,
            message="Failed to update user",
            error=str(e)
        )


@router.delete("/{user_id}", response_model=APIResponse)
async def disable_user(user_id: int, db: Session = Depends(get_db)):
    """
    Disable user (soft delete)

    INPUT:
        user_id: int - User ID

    OUTPUT:
        {
            'success': bool,
            'message': str
        }
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return create_response(
                success=False,
                message=f"User {user_id} not found",
                error="User not found"
            )

        user.is_active = False
        db.commit()

        return create_response(
            success=True,
            message=f"User '{user.username}' disabled successfully",
            data={'user_id': user_id}
        )
    except Exception as e:
        db.rollback()
        return create_response(
            success=False,
            message="Failed to disable user",
            error=str(e)
        )


@router.post("/{user_id}/enable", response_model=APIResponse)
async def enable_user(user_id: int, db: Session = Depends(get_db)):
    """
    Enable user

    INPUT:
        user_id: int - User ID

    OUTPUT:
        {
            'success': bool,
            'message': str
        }
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return create_response(
                success=False,
                message=f"User {user_id} not found",
                error="User not found"
            )

        user.is_active = True
        db.commit()

        return create_response(
            success=True,
            message=f"User '{user.username}' enabled successfully",
            data={'user_id': user_id}
        )
    except Exception as e:
        db.rollback()
        return create_response(
            success=False,
            message="Failed to enable user",
            error=str(e)
        )
