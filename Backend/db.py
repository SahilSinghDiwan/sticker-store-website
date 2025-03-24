from pymongo import MongoClient
import os
from datetime import datetime

client = MongoClient(os.getenv("MONGO_URI"))
db = client["auth_db"]

# Existing collections
users_collection = db["users"]
revoked_tokens_collection = db["revoked_tokens"]
products_collection = db["products"]
cart_collection = db["carts"]
orders_collection = db["orders"]

# New collections
payments_collection = db["payments"]
product_categories_collection = db["product_categories"]

# Create indexes
def setup_indexes():
    # Orders index
    orders_collection.create_index([("user_id", 1)])
    orders_collection.create_index([("created_at", -1)])
    
    # Payments index
    payments_collection.create_index([("order_id", 1)])
    payments_collection.create_index([("status", 1)])
    
    # Categories index
    product_categories_collection.create_index([("name", 1)], unique=True)
    
    # Products index
    products_collection.create_index([("category_id", 1)])
    products_collection.create_index([("name", "text"), ("description", "text")])

# Call this function when the app starts
setup_indexes()
