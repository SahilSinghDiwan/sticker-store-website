from datetime import datetime
from bson import ObjectId
from db import payments_collection, orders_collection

def create_payment(order_id, amount, payment_method, status="pending"):
    """Create a new payment record"""
    payment = {
        "order_id": order_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = payments_collection.insert_one(payment)
    payment["_id"] = str(result.inserted_id)
    
    # Update order with payment reference
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"payment_id": payment["_id"]}}
    )
    
    return payment

def update_payment_status(payment_id, status):
    """Update payment status"""
    payment = payments_collection.find_one_and_update(
        {"_id": ObjectId(payment_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    if payment:
        payment["_id"] = str(payment["_id"])
        
        # Update order status based on payment status
        if status == "completed":
            orders_collection.update_one(
                {"payment_id": payment["_id"]},
                {"$set": {"status": "paid"}}
            )
        elif status == "failed":
            orders_collection.update_one(
                {"payment_id": payment["_id"]},
                {"$set": {"status": "payment_failed"}}
            )
    
    return payment

def get_payment(payment_id):
    """Get payment by ID"""
    payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
    if payment:
        payment["_id"] = str(payment["_id"])
    return payment

def get_order_payment(order_id):
    """Get payment for an order"""
    payment = payments_collection.find_one({"order_id": order_id})
    if payment:
        payment["_id"] = str(payment["_id"])
    return payment 