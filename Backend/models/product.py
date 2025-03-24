from datetime import datetime
from bson import ObjectId
from typing import Dict, Any, Optional

class Product:
    def __init__(self, name: str, price: float, description: str, category_id: str,
                 image_url: str = None, stock: int = 0, active: bool = True):
        self.name = name
        self.price = price
        self.description = description
        self.category_id = ObjectId(category_id)
        self.image_url = image_url
        self.stock = stock
        self.active = active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'stock': self.stock,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Product':
        return Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            category_id=str(data['category_id']),
            image_url=data.get('image_url'),
            stock=data.get('stock', 0),
            active=data.get('active', True)
        ) 