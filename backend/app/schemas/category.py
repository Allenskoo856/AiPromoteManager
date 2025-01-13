from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# 共享属性
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

# 创建分类
class CategoryCreate(CategoryBase):
    pass

# 更新分类
class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

# API 返回的分类信息
class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 包含子分类的分类信息
class CategoryTree(Category):
    children: List["CategoryTree"] = []

    class Config:
        from_attributes = True 