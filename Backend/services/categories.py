from datetime import datetime
from bson import ObjectId
from db import product_categories_collection, products_collection

def create_category(name, description=None):
    """Create a new product category"""
    category = {
        "name": name,
        "description": description,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = product_categories_collection.insert_one(category)
    category["_id"] = str(result.inserted_id)
    return category

def get_categories():
    """Get all categories"""
    categories = list(product_categories_collection.find())
    for category in categories:
        category["_id"] = str(category["_id"])
        # Get product count for each category
        category["product_count"] = products_collection.count_documents(
            {"category_id": category["_id"]}
        )
    return categories

def update_category(category_id, updates):
    """Update a category"""
    updates["updated_at"] = datetime.utcnow()
    product_categories_collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": updates}
    )
    return get_category(category_id)

def delete_category(category_id):
    """Delete a category and update associated products"""
    # First, update all products in this category to have no category
    products_collection.update_many(
        {"category_id": category_id},
        {"$unset": {"category_id": ""}}
    )
    
    # Then delete the category
    result = product_categories_collection.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0

def get_category(category_id):
    """Get a single category by ID"""
    category = product_categories_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        category["_id"] = str(category["_id"])
        category["product_count"] = products_collection.count_documents(
            {"category_id": category["_id"]}
        )
    return category 