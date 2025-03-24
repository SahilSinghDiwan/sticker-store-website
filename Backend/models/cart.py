from datetime import datetime
from bson import ObjectId
from typing import Dict, Any, List, Optional

class Cart:
    def __init__(self, user_id: str, items: Optional[List[Dict[str, Any]]] = None):
        self.user_id = ObjectId(user_id)
        self.items = items or []  # List of {product_id, quantity, price}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'items': self.items,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def add_item(self, product_id: str, quantity: int, price: float) -> None:
        # Check if item already exists
        for item in self.items:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                self.updated_at = datetime.utcnow()
                return

        # Add new item
        self.items.append({
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        })
        self.updated_at = datetime.utcnow()

    def update_item(self, product_id: str, quantity: int) -> None:
        for item in self.items:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                self.updated_at = datetime.utcnow()
                return
        raise ValueError(f"Product {product_id} not found in cart")

    def remove_item(self, product_id: str) -> None:
        self.items = [item for item in self.items if item['product_id'] != product_id]
        self.updated_at = datetime.utcnow()

    def clear(self) -> None:
        self.items = []
        self.updated_at = datetime.utcnow()

    def get_total(self) -> float:
        return sum(item['price'] * item['quantity'] for item in self.items)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Cart':
        return Cart(
            user_id=str(data['user_id']),
            items=data.get('items', [])
        ) 