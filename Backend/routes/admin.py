from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from ..middleware.admin import admin_required
from ..db import products_collection, orders_collection, users_collection
from bson import ObjectId

router = APIRouter(prefix="/admin", dependencies=[Depends(admin_required)])

# Models
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    image_url: str

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    stock: Optional[int]
    image_url: Optional[str]

class OrderUpdate(BaseModel):
    status: str
    tracking_number: Optional[str]

class UserUpdate(BaseModel):
    role: Optional[str]
    is_active: Optional[bool]

# Product Management
@router.get("/products")
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None
) -> Dict:
    """Get all products with pagination"""
    query = {}
    if category:
        query["category"] = category
        
    total = await products_collection.count_documents(query)
    products = await products_collection.find(query).skip(skip).limit(limit).to_list(None)
    
    return {
        "total": total,
        "products": products,
        "page": skip // limit + 1,
        "pages": (total + limit - 1) // limit
    }

@router.post("/products")
async def create_product(product: ProductCreate) -> Dict:
    """Create a new product"""
    result = await products_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id), "message": "Product created successfully"}

@router.put("/products/{product_id}")
async def update_product(product_id: str, product: ProductUpdate) -> Dict:
    """Update a product"""
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@router.delete("/products/{product_id}")
async def delete_product(product_id: str) -> Dict:
    """Delete a product"""
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Order Management
@router.get("/orders")
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
) -> Dict:
    """Get all orders with pagination"""
    query = {}
    if status:
        query["status"] = status
        
    total = await orders_collection.count_documents(query)
    orders = await orders_collection.find(query).skip(skip).limit(limit).to_list(None)
    
    return {
        "total": total,
        "orders": orders,
        "page": skip // limit + 1,
        "pages": (total + limit - 1) // limit
    }

@router.put("/orders/{order_id}")
async def update_order(order_id: str, order: OrderUpdate) -> Dict:
    """Update order status and tracking"""
    result = await orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": order.dict(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order updated successfully"}

# User Management
@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[str] = None
) -> Dict:
    """Get all users with pagination"""
    query = {}
    if role:
        query["role"] = role
        
    total = await users_collection.count_documents(query)
    users = await users_collection.find(query, {"password": 0}).skip(skip).limit(limit).to_list(None)
    
    return {
        "total": total,
        "users": users,
        "page": skip // limit + 1,
        "pages": (total + limit - 1) // limit
    }

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate) -> Dict:
    """Update user role and status"""
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

# Analytics
@router.get("/analytics/dashboard")
async def get_dashboard_analytics() -> Dict:
    """Get dashboard analytics"""
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    # Revenue analytics
    recent_orders = await orders_collection.find({
        "created_at": {"$gte": thirty_days_ago},
        "status": "completed"
    }).to_list(None)
    
    total_revenue = sum(order.get("total", 0) for order in recent_orders)
    order_count = len(recent_orders)
    
    # Product analytics
    top_products = await products_collection.find().sort("sales_count", -1).limit(5).to_list(None)
    low_stock_products = await products_collection.find({"stock": {"$lt": 10}}).to_list(None)
    
    # User analytics
    total_users = await users_collection.count_documents({})
    new_users = await users_collection.count_documents({"created_at": {"$gte": thirty_days_ago}})
    
    return {
        "revenue": {
            "total": total_revenue,
            "order_count": order_count,
            "average_order_value": total_revenue / order_count if order_count > 0 else 0
        },
        "products": {
            "top_selling": top_products,
            "low_stock": low_stock_products
        },
        "users": {
            "total": total_users,
            "new_last_30_days": new_users
        }
    }