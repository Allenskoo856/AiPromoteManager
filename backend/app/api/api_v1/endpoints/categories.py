from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_category
from app.schemas import category as category_schema
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[category_schema.Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取所有分类。
    """
    categories = crud_category.get_multi(db, skip=skip, limit=limit)
    return categories

@router.get("/tree", response_model=List[Dict])
def read_category_tree(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取分类树。
    """
    return crud_category.get_full_tree(db=db, skip=skip, limit=limit)

@router.get("/root", response_model=List[category_schema.Category])
def read_root_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取根分类。
    """
    categories = crud_category.get_root_categories(
        db=db, skip=skip, limit=limit
    )
    return categories

@router.get("/{category_id}/children", response_model=List[category_schema.Category])
def read_category_children(
    *,
    db: Session = Depends(get_db),
    category_id: int,
) -> Any:
    """
    获取子分类。
    """
    return crud_category.get_children(db=db, parent_id=category_id)

@router.post("/", response_model=category_schema.Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: category_schema.CategoryCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新分类。
    """
    category = crud_category.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="The category with this name already exists.",
        )
    if category_in.parent_id:
        parent = crud_category.get(db=db, id=category_in.parent_id)
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found",
            )
    category = crud_category.create(db=db, obj_in=category_in)
    return category

@router.put("/{category_id}", response_model=category_schema.Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: category_schema.CategoryUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新分类。
    """
    category = crud_category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category_in.parent_id:
        parent = crud_category.get(db=db, id=category_in.parent_id)
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found",
            )
        # 检查是否会形成循环依赖
        if category_id == category_in.parent_id:
            raise HTTPException(
                status_code=400,
                detail="A category cannot be its own parent",
            )
    category = crud_category.update(db=db, db_obj=category, obj_in=category_in)
    return category

@router.delete("/{category_id}")
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除分类。
    """
    category = crud_category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    # 检查是否有子分类
    children = crud_category.get_children(db=db, parent_id=category_id)
    if children:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with children",
        )
    category = crud_category.remove(db=db, id=category_id)
    return {"status": "success"} 