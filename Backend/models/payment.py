from datetime import datetime
from enum import Enum
from bson import ObjectId
from typing import Dict, Any, Optional

class PaymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

class Payment:
    def __init__(
        self,
        order_id: str,
        amount: float,
        currency: str = "USD",
        payment_method: PaymentMethod = PaymentMethod.STRIPE,
        status: PaymentStatus = PaymentStatus.PENDING,
        stripe_payment_intent_id: Optional[str] = None,
        _id: Optional[str] = None
    ):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.order_id = ObjectId(order_id)
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.status = status
        self.stripe_payment_intent_id = stripe_payment_intent_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.completed_at = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            '_id': self._id,
            'order_id': self.order_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method.value,
            'status': self.status.value,
            'stripe_payment_intent_id': self.stripe_payment_intent_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at
        }

    def update_status(self, status: PaymentStatus) -> None:
        self.status = status
        self.updated_at = datetime.utcnow()
        if status == PaymentStatus.COMPLETED:
            self.completed_at = datetime.utcnow()

    def set_stripe_payment_intent(self, payment_intent_id: str) -> None:
        self.stripe_payment_intent_id = payment_intent_id
        self.updated_at = datetime.utcnow()

    def process_refund(self) -> None:
        self.status = PaymentStatus.REFUNDED
        self.updated_at = datetime.utcnow()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Payment':
        return Payment(
            order_id=str(data['order_id']),
            amount=data['amount'],
            currency=data.get('currency', 'USD'),
            payment_method=PaymentMethod(data.get('payment_method', 'stripe')),
            status=PaymentStatus(data.get('status', 'pending')),
            stripe_payment_intent_id=data.get('stripe_payment_intent_id'),
            _id=str(data['_id']) if data.get('_id') else None
        ) 