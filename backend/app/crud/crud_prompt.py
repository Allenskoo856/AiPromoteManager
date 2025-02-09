from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.models import Prompt, Tag, Version
from app.schemas.prompt import PromptCreate, PromptUpdate

class CRUDPrompt(CRUDBase[Prompt, PromptCreate, PromptUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PromptCreate, owner_id: int
    ) -> Prompt:
        obj_in_data = obj_in.dict(exclude={"tag_ids"})
        db_obj = Prompt(**obj_in_data, owner_id=owner_id)
        
        if obj_in.tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(obj_in.tag_ids)).all()
            db_obj.tags = tags
            
        # 创建第一个版本
        version = Version(
            content=obj_in.content,
            version_number=1
        )
        db_obj.versions.append(version)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Prompt,
        obj_in: Union[PromptUpdate, Dict[str, Any]]
    ) -> Prompt:
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # 如果内容发生变化，创建新版本
        if "content" in update_data and update_data["content"] != db_obj.content:
            latest_version = max(db_obj.versions, key=lambda x: x.version_number)
            new_version = Version(
                content=update_data["content"],
                version_number=latest_version.version_number + 1
            )
            db_obj.versions.append(new_version)

        # 更新标签
        if "tag_ids" in update_data:
            tag_ids = update_data.pop("tag_ids", [])
            tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            db_obj.tags = tags

        # 更新其他字段
        for field in ["title", "content", "description", "is_public", "category_id"]:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: Any) -> Optional[Prompt]:
        return db.query(self.model).options(joinedload(self.model.category)).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, search: Optional[str] = None
    ) -> List[Prompt]:
        query = db.query(self.model).options(joinedload(self.model.category))
        
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
            
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (self.model.title.ilike(search_pattern)) |
                (self.model.content.ilike(search_pattern))
            )
            
        return query.offset(skip).limit(limit).all()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100,
        category_id: Optional[int] = None, search: Optional[str] = None
    ) -> List[Prompt]:
        query = db.query(self.model).options(
            joinedload(self.model.category),
            joinedload(self.model.tags)
        )
        query = query.filter(Prompt.owner_id == owner_id)
        
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
            
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (self.model.title.ilike(search_pattern)) |
                (self.model.content.ilike(search_pattern))
            )
            
        return query.offset(skip).limit(limit).all()

    def get_public(
        self, db: Session, *, skip: int = 0, limit: int = 100,
        category_id: Optional[int] = None, search: Optional[str] = None
    ) -> List[Prompt]:
        query = db.query(self.model).options(joinedload(self.model.category))
        query = query.filter(Prompt.is_public == True)
        
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
            
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (self.model.title.ilike(search_pattern)) |
                (self.model.content.ilike(search_pattern))
            )
        
        return query.offset(skip).limit(limit).all()

    def get_count_by_user(self, db: Session, user_id: int) -> int:
        """
        获取用户创建的提示词数量
        """
        return db.query(func.count(Prompt.id)).filter(Prompt.owner_id == user_id).scalar() or 0

crud_prompt = CRUDPrompt(Prompt)