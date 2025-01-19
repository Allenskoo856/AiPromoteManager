from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from app.crud import crud_user, crud_prompt, crud_category, crud_tag, crud_share
from app.schemas import user as user_schema
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.post("/", response_model=user_schema.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schema.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=user_schema.User)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.patch("/me", response_model=user_schema.User)
@router.put("/me", response_model=user_schema.User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
    user_in: user_schema.UserUpdate,
) -> Any:
    """
    Update own user.
    """
    try:
        user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/me/stats", response_model=user_schema.UserStats)
def get_user_stats(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户的统计信息。
    """
    prompt_count = crud_prompt.get_count_by_user(db, user_id=current_user.id)
    category_count = crud_category.get_count_by_user(db, user_id=current_user.id)
    tag_count = crud_tag.get_count_by_user(db, user_id=current_user.id)
    share_count = crud_share.get_count_by_user(db, user_id=current_user.id)
    
    return {
        "prompt_count": prompt_count,
        "category_count": category_count,
        "tag_count": tag_count,
        "share_count": share_count
    } 