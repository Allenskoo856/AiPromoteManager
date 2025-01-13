from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from .tag import Tag
from .version import Version

# Category 简化模型
class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# 共享属性
class PromptBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    is_public: bool = False
    category_id: Optional[int] = None

# 创建提示词
class PromptCreate(PromptBase):
    tag_ids: Optional[List[int]] = None

# 更新提示词
class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

# API 返回的提示词信息
class Prompt(PromptBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryBase] = None

    class Config:
        from_attributes = True

# 提示词详细信息（包含标签和版本）
class PromptDetail(Prompt):
    tags: List[Tag] = []
    versions: List[Version] = []

    class Config:
        from_attributes = True 