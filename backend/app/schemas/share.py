from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 共享属性
class ShareBase(BaseModel):
    prompt_id: int
    can_edit: bool = False
    expires_at: Optional[datetime] = None
    password: Optional[str] = None

# 创建分享
class ShareCreate(ShareBase):
    pass

# 更新分享
class ShareUpdate(ShareBase):
    prompt_id: Optional[int] = None

# API 返回的分享信息
class Share(ShareBase):
    id: int
    user_id: int
    share_token: str
    created_at: datetime

    class Config:
        from_attributes = True 