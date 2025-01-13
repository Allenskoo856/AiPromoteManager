from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_prompt
from app.schemas import prompt as prompt_schema
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[prompt_schema.Prompt])
def read_prompts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: int = Query(None, description="按分类ID过滤"),
    search: str = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户的所有提示词。
    支持按分类过滤和关键词搜索。
    """
    prompts = crud_prompt.get_multi_by_owner(
        db=db, 
        owner_id=current_user.id, 
        skip=skip, 
        limit=limit,
        category_id=category_id,
        search=search
    )
    return prompts

@router.post("/", response_model=prompt_schema.Prompt)
def create_prompt(
    *,
    db: Session = Depends(get_db),
    prompt_in: prompt_schema.PromptCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新的提示词。
    """
    prompt = crud_prompt.create_with_owner(
        db=db, obj_in=prompt_in, owner_id=current_user.id
    )
    return prompt

@router.get("/public", response_model=List[prompt_schema.Prompt])
def read_public_prompts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: int = Query(None, description="按分类ID过滤"),
    search: str = Query(None, description="搜索关键词"),
) -> Any:
    """
    获取所有公开的提示词。
    支持按分类过滤和关键词搜索。
    """
    prompts = crud_prompt.get_public(
        db=db, 
        skip=skip, 
        limit=limit,
        category_id=category_id,
        search=search
    )
    return prompts

@router.get("/{prompt_id}", response_model=prompt_schema.PromptDetail)
def read_prompt(
    *,
    db: Session = Depends(get_db),
    prompt_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    通过ID获取提示词。
    """
    prompt = crud_prompt.get(db=db, id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if not prompt.is_public and (prompt.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return prompt

@router.put("/{prompt_id}", response_model=prompt_schema.Prompt)
def update_prompt(
    *,
    db: Session = Depends(get_db),
    prompt_id: int,
    prompt_in: prompt_schema.PromptUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新提示词。
    """
    prompt = crud_prompt.get(db=db, id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    prompt = crud_prompt.update(db=db, db_obj=prompt, obj_in=prompt_in)
    return prompt

@router.delete("/{prompt_id}")
def delete_prompt(
    *,
    db: Session = Depends(get_db),
    prompt_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除提示词。
    """
    prompt = crud_prompt.get(db=db, id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    prompt = crud_prompt.remove(db=db, id=prompt_id)
    return {"status": "success"} 