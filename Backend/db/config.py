from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'sticker_shop')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Initialize collections
products_collection = db.products
orders_collection = db.orders
carts_collection = db.carts
categories_collection = db.categories
users_collection = db.users

# Create indexes
def init_db():
    # Products indexes
    products_collection.create_index('name')
    products_collection.create_index('category_id')
    products_collection.create_index('price')
    
    # Orders indexes
    orders_collection.create_index('user_id')
    orders_collection.create_index('created_at')
    orders_collection.create_index('status')
    
    # Carts indexes
    carts_collection.create_index('user_id', unique=True)
    
    # Categories indexes
    categories_collection.create_index('name', unique=True)
    
    # Users indexes
    users_collection.create_index('email', unique=True)
    users_collection.create_index('provider_id')

# Call init_db when starting the application
init_db() 