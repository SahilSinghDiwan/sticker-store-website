from datetime import datetime
from bson import ObjectId
from typing import Dict, Any, List
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Order:
    def __init__(self, user_id: str, items: List[Dict[str, Any]], total: float,
                 shipping_address: Dict[str, str], status: str = OrderStatus.PENDING.value):
        self.user_id = ObjectId(user_id)
        self.items = items  # List of {product_id, quantity, price, product_details}
        self.total = total
        self.shipping_address = shipping_address
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.shipping_status = "pending"
        self.payment_info = {
            "status": "pending",
            "payment_method": None,
            "transaction_id": None
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'items': self.items,
            'total': self.total,
            'shipping_address': self.shipping_address,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'shipping_status': self.shipping_status,
            'payment_info': self.payment_info
        }

    def update_status(self, status: str) -> None:
        if status not in [s.value for s in OrderStatus]:
            raise ValueError(f"Invalid status: {status}")
        self.status = status
        self.updated_at = datetime.utcnow()

    def update_payment(self, payment_method: str, transaction_id: str) -> None:
        self.payment_info = {
            "status": "completed",
            "payment_method": payment_method,
            "transaction_id": transaction_id
        }
        self.updated_at = datetime.utcnow()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Order':
        return Order(
            user_id=str(data['user_id']),
            items=data['items'],
            total=data['total'],
            shipping_address=data['shipping_address'],
            status=data.get('status', OrderStatus.PENDING.value)
        ) 