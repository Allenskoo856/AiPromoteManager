from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 共享属性
class TagBase(BaseModel):
    name: str

# 创建标签
class TagCreate(TagBase):
    pass

# 更新标签
class TagUpdate(TagBase):
    name: Optional[str] = None

# API 返回的标签信息
class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 