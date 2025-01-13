from typing import List, Optional
from sqlalchemy.orm import Session
import secrets
from app.crud.base import CRUDBase
from app.models.models import Share
from app.schemas.share import ShareCreate, ShareUpdate

class CRUDShare(CRUDBase[Share, ShareCreate, ShareUpdate]):
    def get_by_token(self, db: Session, *, token: str) -> Optional[Share]:
        return db.query(Share).filter(Share.share_token == token).first()

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Share]:
        return (
            db.query(Share)
            .filter(Share.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
        self, db: Session, *, obj_in: ShareCreate, user_id: int
    ) -> Share:
        share_token = secrets.token_urlsafe(32)
        db_obj = Share(
            **obj_in.dict(),
            user_id=user_id,
            share_token=share_token,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_share = CRUDShare(Share) 