from typing import Dict, Any, List, Optional
from bson import ObjectId
from datetime import datetime
from ..db.config import orders_collection, products_collection, carts_collection
from ..models.order import Order, OrderStatus
from . import cart as cart_service

async def create_order(
    user_id: str,
    shipping_address: Dict[str, str]
) -> Dict[str, Any]:
    """Create a new order from user's cart"""
    # Get user's cart
    cart_data = await cart_service.get_user_cart(user_id)
    if not cart_data or not cart_data.get('items'):
        raise ValueError("Cart is empty")

    # Validate stock and prepare items
    order_items = []
    total = 0
    
    for item in cart_data['items']:
        product = await products_collection.find_one({'_id': ObjectId(item['product_id'])})
        if not product:
            raise ValueError(f"Product {item['product_id']} not found")
        
        if product['stock'] < item['quantity']:
            raise ValueError(f"Insufficient stock for product {product['name']}")
        
        # Prepare order item with product details
        order_item = {
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'price': product['price'],
            'product_details': {
                'name': product['name'],
                'description': product['description'],
                'image_url': product.get('image_url')
            }
        }
        order_items.append(order_item)
        total += item['quantity'] * product['price']

    # Create order
    order = Order(
        user_id=user_id,
        items=order_items,
        total=total,
        shipping_address=shipping_address
    )
    
    # Insert order
    order_dict = order.to_dict()
    result = await orders_collection.insert_one(order_dict)
    order_dict['_id'] = result.inserted_id

    # Update product stock
    for item in order_items:
        await products_collection.update_one(
            {'_id': ObjectId(item['product_id'])},
            {'$inc': {'stock': -item['quantity']}}
        )

    # Clear cart
    await cart_service.clear_cart(user_id)

    return order_dict

async def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    """Get order by ID"""
    order_data = await orders_collection.find_one({'_id': ObjectId(order_id)})
    if order_data:
        order = Order.from_dict(order_data)
        return order.to_dict()
    return None

async def get_user_orders(
    user_id: str,
    status: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
) -> List[Dict[str, Any]]:
    """Get orders for a specific user"""
    query = {'user_id': ObjectId(user_id)}
    if status:
        query['status'] = status

    cursor = orders_collection.find(query) \
        .sort('created_at', -1) \
        .skip(skip) \
        .limit(limit)
    
    orders = []
    async for order_data in cursor:
        order = Order.from_dict(order_data)
        orders.append(order.to_dict())
    
    return orders

async def update_order_status(order_id: str, status: str) -> Dict[str, Any]:
    """Update order status"""
    if status not in [s.value for s in OrderStatus]:
        raise ValueError(f"Invalid status: {status}")

    order_data = await get_order(order_id)
    if not order_data:
        raise ValueError("Order not found")

    order = Order.from_dict(order_data)
    order.update_status(status)
    
    await orders_collection.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {
            'status': status,
            'updated_at': datetime.utcnow()
        }}
    )
    
    return order.to_dict()

async def update_shipping_status(order_id: str, shipping_status: str) -> Dict[str, Any]:
    """Update order shipping status"""
    order_data = await get_order(order_id)
    if not order_data:
        raise ValueError("Order not found")

    await orders_collection.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {
            'shipping_status': shipping_status,
            'updated_at': datetime.utcnow()
        }}
    )
    
    return await get_order(order_id)

async def cancel_order(order_id: str) -> Dict[str, Any]:
    """Cancel an order and restore product stock"""
    order_data = await get_order(order_id)
    if not order_data:
        raise ValueError("Order not found")

    if order_data['status'] not in [OrderStatus.PENDING.value, OrderStatus.PAID.value]:
        raise ValueError("Order cannot be cancelled in current status")

    # Restore product stock
    for item in order_data['items']:
        await products_collection.update_one(
            {'_id': ObjectId(item['product_id'])},
            {'$inc': {'stock': item['quantity']}}
        )

    # Update order status
    return await update_order_status(order_id, OrderStatus.CANCELLED.value) 