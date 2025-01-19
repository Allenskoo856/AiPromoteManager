from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# 共享属性
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True

# 创建用户时需要的属性
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

# 更新用户时可以更新的属性
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

    class Config:
        from_attributes = True

# API 返回的用户信息
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 

# 用户统计信息
class UserStats(BaseModel):
    prompt_count: int
    category_count: int
    tag_count: int
    share_count: int 