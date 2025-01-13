from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.models import Tag
from app.schemas.tag import TagCreate, TagUpdate

class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Tag]:
        return db.query(Tag).filter(Tag.name == name).first()

    def get_multi_by_ids(
        self, db: Session, *, ids: List[int]
    ) -> List[Tag]:
        return db.query(Tag).filter(Tag.id.in_(ids)).all()

    def get_count_by_user(self, db: Session, user_id: int) -> int:
        """
        获取用户创建的标签数量
        """
        return db.query(func.count(Tag.id)).filter(Tag.owner_id == user_id).scalar() or 0

crud_tag = CRUDTag(Tag) 