from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_share
from app.schemas import share as share_schema
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[share_schema.Share])
def read_shares(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户的所有分享。
    """
    shares = crud_share.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return shares

@router.post("/", response_model=share_schema.Share)
def create_share(
    *,
    db: Session = Depends(get_db),
    share_in: share_schema.ShareCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新的分享。
    """
    share = crud_share.create_with_user(
        db=db, obj_in=share_in, user_id=current_user.id
    )
    return share

@router.get("/{share_id}", response_model=share_schema.Share)
def read_share(
    *,
    db: Session = Depends(get_db),
    share_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    通过ID获取分享。
    """
    share = crud_share.get(db=db, id=share_id)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    if share.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return share

@router.delete("/{share_id}")
def delete_share(
    *,
    db: Session = Depends(get_db),
    share_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除分享。
    """
    share = crud_share.get(db=db, id=share_id)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    if share.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    share = crud_share.remove(db=db, id=share_id)
    return {"status": "success"} 