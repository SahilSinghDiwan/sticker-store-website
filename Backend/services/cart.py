from typing import Dict, Any, Optional, List
from bson import ObjectId
from ..db.config import carts_collection, products_collection
from ..models.cart import Cart

async def get_user_cart(user_id: str) -> Optional[Dict[str, Any]]:
    """Get cart for a specific user"""
    cart_data = await carts_collection.find_one({'user_id': ObjectId(user_id)})
    if cart_data:
        cart = Cart.from_dict(cart_data)
        return cart.to_dict()
    return None

async def create_cart(user_id: str) -> Dict[str, Any]:
    """Create a new cart for a user"""
    cart = Cart(user_id=user_id)
    cart_dict = cart.to_dict()
    await carts_collection.insert_one(cart_dict)
    return cart_dict

async def add_item_to_cart(user_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
    """Add an item to the user's cart"""
    # Get product details
    product = await products_collection.find_one({'_id': ObjectId(product_id)})
    if not product:
        raise ValueError("Product not found")
    
    if product['stock'] < quantity:
        raise ValueError("Insufficient stock")

    # Get or create cart
    cart_data = await get_user_cart(user_id)
    if not cart_data:
        cart_data = await create_cart(user_id)
    
    cart = Cart.from_dict(cart_data)
    cart.add_item(product_id, quantity, product['price'])
    
    # Update cart in database
    await carts_collection.update_one(
        {'user_id': ObjectId(user_id)},
        {'$set': cart.to_dict()}
    )
    
    return cart.to_dict()

async def update_cart_item(user_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
    """Update quantity of an item in the cart"""
    cart_data = await get_user_cart(user_id)
    if not cart_data:
        raise ValueError("Cart not found")
    
    # Check product stock
    product = await products_collection.find_one({'_id': ObjectId(product_id)})
    if not product:
        raise ValueError("Product not found")
    
    if product['stock'] < quantity:
        raise ValueError("Insufficient stock")
    
    cart = Cart.from_dict(cart_data)
    cart.update_item(product_id, quantity)
    
    await carts_collection.update_one(
        {'user_id': ObjectId(user_id)},
        {'$set': cart.to_dict()}
    )
    
    return cart.to_dict()

async def remove_item_from_cart(user_id: str, product_id: str) -> Dict[str, Any]:
    """Remove an item from the cart"""
    cart_data = await get_user_cart(user_id)
    if not cart_data:
        raise ValueError("Cart not found")
    
    cart = Cart.from_dict(cart_data)
    cart.remove_item(product_id)
    
    await carts_collection.update_one(
        {'user_id': ObjectId(user_id)},
        {'$set': cart.to_dict()}
    )
    
    return cart.to_dict()

async def clear_cart(user_id: str) -> Dict[str, Any]:
    """Clear all items from the cart"""
    cart_data = await get_user_cart(user_id)
    if not cart_data:
        raise ValueError("Cart not found")
    
    cart = Cart.from_dict(cart_data)
    cart.clear()
    
    await carts_collection.update_one(
        {'user_id': ObjectId(user_id)},
        {'$set': cart.to_dict()}
    )
    
    return cart.to_dict()

async def get_cart_total(user_id: str) -> float:
    """Get the total value of items in the cart"""
    cart_data = await get_user_cart(user_id)
    if not cart_data:
        return 0.0
    
    cart = Cart.from_dict(cart_data)
    return cart.get_total()
