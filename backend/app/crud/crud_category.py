from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    def get_root_categories(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        return (
            db.query(Category)
            .filter(Category.parent_id == None)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_children(
        self, db: Session, *, parent_id: int
    ) -> List[Category]:
        return (
            db.query(Category)
            .filter(Category.parent_id == parent_id)
            .all()
        )

    def get_tree(self, db: Session, *, category: Category) -> Dict:
        """获取分类树"""
        result = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "parent_id": category.parent_id,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
            "children": []
        }
        
        children = self.get_children(db=db, parent_id=category.id)
        if children:
            result["children"] = [
                self.get_tree(db=db, category=child)
                for child in children
            ]
        
        return result

    def get_full_tree(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Dict]:
        """获取完整的分类树"""
        root_categories = self.get_root_categories(
            db=db, skip=skip, limit=limit
        )
        return [
            self.get_tree(db=db, category=category)
            for category in root_categories
        ]

    def get_count_by_user(self, db: Session, user_id: int) -> int:
        """
        获取用户的提示词使用了多少个不同的分类
        """
        from app.models.models import Prompt
        return db.query(func.count(func.distinct(Prompt.category_id)))\
            .filter(Prompt.owner_id == user_id)\
            .scalar() or 0

crud_category = CRUDCategory(Category) 