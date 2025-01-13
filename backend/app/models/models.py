from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# 提示词和标签的多对多关系表
prompt_tag = Table(
    'prompt_tag',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    prompts = relationship("Prompt", back_populates="owner")
    shares = relationship("Share", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(200))
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    prompts = relationship("Prompt", back_populates="category")
    children = relationship("Category")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    prompts = relationship("Prompt", secondary=prompt_tag, back_populates="tags")

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    content = Column(Text)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    owner = relationship("User", back_populates="prompts")
    category = relationship("Category", back_populates="prompts")
    tags = relationship("Tag", secondary=prompt_tag, back_populates="prompts")
    versions = relationship("Version", back_populates="prompt")
    shares = relationship("Share", back_populates="prompt")

class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    content = Column(Text)
    version_number = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    prompt = relationship("Prompt", back_populates="versions")

class Share(Base):
    __tablename__ = "shares"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    share_token = Column(String(100), unique=True, index=True)
    can_edit = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    password = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    prompt = relationship("Prompt", back_populates="shares")
    user = relationship("User", back_populates="shares") 