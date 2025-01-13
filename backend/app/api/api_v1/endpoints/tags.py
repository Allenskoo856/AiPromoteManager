from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_tag
from app.schemas import tag as tag_schema
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[tag_schema.Tag])
def read_tags(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取所有标签。
    """
    tags = crud_tag.get_multi(db, skip=skip, limit=limit)
    return tags

@router.post("/", response_model=tag_schema.Tag)
def create_tag(
    *,
    db: Session = Depends(get_db),
    tag_in: tag_schema.TagCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新标签。
    """
    tag = crud_tag.get_by_name(db, name=tag_in.name)
    if tag:
        raise HTTPException(
            status_code=400,
            detail="The tag with this name already exists.",
        )
    tag = crud_tag.create(db=db, obj_in=tag_in)
    return tag

@router.put("/{tag_id}", response_model=tag_schema.Tag)
def update_tag(
    *,
    db: Session = Depends(get_db),
    tag_id: int,
    tag_in: tag_schema.TagUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新标签。
    """
    tag = crud_tag.get(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud_tag.update(db=db, db_obj=tag, obj_in=tag_in)
    return tag

@router.delete("/{tag_id}")
def delete_tag(
    *,
    db: Session = Depends(get_db),
    tag_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除标签。
    """
    tag = crud_tag.get(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud_tag.remove(db=db, id=tag_id)
    return {"status": "success"} 