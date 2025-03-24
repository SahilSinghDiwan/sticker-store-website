from datetime import datetime
from bson import ObjectId
from typing import Dict, Any, Optional

class Category:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        parent_id: Optional[str] = None,
        product_count: int = 0,
        _id: Optional[str] = None
    ):
        self.name = name
        self.description = description
        self.parent_id = ObjectId(parent_id) if parent_id else None
        self.product_count = product_count
        self._id = ObjectId(_id) if _id else ObjectId()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            '_id': self._id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'product_count': self.product_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def increment_product_count(self, amount: int = 1) -> None:
        self.product_count += amount
        self.updated_at = datetime.utcnow()

    def decrement_product_count(self, amount: int = 1) -> None:
        self.product_count = max(0, self.product_count - amount)
        self.updated_at = datetime.utcnow()

    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        if name:
            self.name = name
        if description is not None:  # Allow empty string
            self.description = description
        self.updated_at = datetime.utcnow()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Category':
        return Category(
            name=data['name'],
            description=data.get('description'),
            parent_id=str(data['parent_id']) if data.get('parent_id') else None,
            product_count=data.get('product_count', 0),
            _id=str(data['_id']) if data.get('_id') else None
        ) 