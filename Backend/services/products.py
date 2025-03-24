import boto3
from bson import ObjectId
from db import products_collection, categories_collection
import os
from datetime import datetime
from PIL import Image
import io
import time
from typing import Dict, Any, List, Optional
from ..models.product import Product

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
IMAGE_SIZES = {
    'regular': (800, 800),
    'thumbnail': (150, 150),
    'preview': (400, 400)
}

def generate_image_key(original_filename, size='regular'):
    """Generate a unique key for S3 storage"""
    timestamp = int(time.time())
    base_name = os.path.splitext(original_filename)[0].lower().replace(' ', '_')
    extension = os.path.splitext(original_filename)[1].lower()
    
    if size == 'regular':
        return f"products/regular/{base_name}_{timestamp}{extension}"
    elif size == 'thumbnail':
        return f"products/thumbnails/{base_name}_{timestamp}_thumb{extension}"
    else:  # preview
        return f"products/previews/{base_name}_{timestamp}_preview{extension}"

def resize_image(image_file, size):
    """Resize image while maintaining aspect ratio"""
    img = Image.open(image_file)
    img.thumbnail(size)
    
    # Convert to buffer
    buffer = io.BytesIO()
    img.save(buffer, format=img.format)
    buffer.seek(0)
    
    return buffer

def upload_product_image(image_file, original_filename):
    """Upload product image in different sizes"""
    image_urls = {}
    
    for size_name, dimensions in IMAGE_SIZES.items():
        # Reset file pointer
        image_file.seek(0)
        
        # Resize image
        resized_image = resize_image(image_file, dimensions)
        
        # Generate key for this size
        key = generate_image_key(original_filename, size_name)
        
        # Upload to S3
        s3_client.upload_fileobj(
            resized_image,
            BUCKET_NAME,
            key,
            ExtraArgs={
                'ContentType': f'image/{Image.open(image_file).format.lower()}',
                'ACL': 'public-read'
            }
        )
        
        # Generate URL
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key
            },
            ExpiresIn=3600
        )
        
        image_urls[size_name] = {
            'key': key,
            'url': url
        }
    
    return image_urls

async def create_product(
    name: str,
    price: float,
    description: str,
    category_id: str,
    image_url: Optional[str] = None,
    stock: int = 0
) -> Dict[str, Any]:
    """Create a new product"""
    # Validate category exists
    category = await categories_collection.find_one({'_id': ObjectId(category_id)})
    if not category:
        raise ValueError("Category not found")

    product = Product(
        name=name,
        price=price,
        description=description,
        category_id=category_id,
        image_url=image_url,
        stock=stock
    )
    
    product_dict = product.to_dict()
    result = await products_collection.insert_one(product_dict)
    product_dict['_id'] = result.inserted_id

    # Increment category product count
    await categories_collection.update_one(
        {'_id': ObjectId(category_id)},
        {'$inc': {'product_count': 1}}
    )

    return product_dict

async def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    """Get product by ID"""
    product_data = await products_collection.find_one({'_id': ObjectId(product_id)})
    if product_data:
        product = Product.from_dict(product_data)
        return product.to_dict()
    return None

async def get_products(
    category_id: Optional[str] = None,
    search_query: Optional[str] = None,
    sort_by: str = 'created_at',
    sort_order: int = -1,
    limit: int = 20,
    skip: int = 0,
    active_only: bool = True
) -> List[Dict[str, Any]]:
    """Get products with optional filtering and sorting"""
    query = {}
    
    if category_id:
        query['category_id'] = ObjectId(category_id)
    
    if search_query:
        query['$or'] = [
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'description': {'$regex': search_query, '$options': 'i'}}
        ]
    
    if active_only:
        query['active'] = True

    cursor = products_collection.find(query) \
        .sort(sort_by, sort_order) \
        .skip(skip) \
        .limit(limit)
    
    products = []
    async for product_data in cursor:
        product = Product.from_dict(product_data)
        products.append(product.to_dict())
    
    return products

async def update_product(
    product_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Update product details"""
    product_data = await get_product(product_id)
    if not product_data:
        raise ValueError("Product not found")

    # Handle category change
    if 'category_id' in updates and updates['category_id'] != str(product_data['category_id']):
        old_category_id = product_data['category_id']
        new_category_id = updates['category_id']
        
        # Validate new category exists
        new_category = await categories_collection.find_one({'_id': ObjectId(new_category_id)})
        if not new_category:
            raise ValueError("New category not found")
        
        # Update category product counts
        await categories_collection.update_one(
            {'_id': ObjectId(old_category_id)},
            {'$inc': {'product_count': -1}}
        )
        await categories_collection.update_one(
            {'_id': ObjectId(new_category_id)},
            {'$inc': {'product_count': 1}}
        )

    updates['updated_at'] = datetime.utcnow()
    await products_collection.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': updates}
    )

    return await get_product(product_id)

async def delete_product(product_id: str) -> bool:
    """Delete a product"""
    product_data = await get_product(product_id)
    if not product_data:
        raise ValueError("Product not found")

    # Decrement category product count
    await categories_collection.update_one(
        {'_id': ObjectId(product_data['category_id'])},
        {'$inc': {'product_count': -1}}
    )

    result = await products_collection.delete_one({'_id': ObjectId(product_id)})
    return result.deleted_count > 0

async def update_stock(product_id: str, quantity: int) -> Dict[str, Any]:
    """Update product stock"""
    product_data = await get_product(product_id)
    if not product_data:
        raise ValueError("Product not found")

    if product_data['stock'] + quantity < 0:
        raise ValueError("Insufficient stock")

    await products_collection.update_one(
        {'_id': ObjectId(product_id)},
        {
            '$inc': {'stock': quantity},
            '$set': {'updated_at': datetime.utcnow()}
        }
    )

    return await get_product(product_id)

async def get_low_stock_products(threshold: int = 10) -> List[Dict[str, Any]]:
    """Get products with stock below threshold"""
    cursor = products_collection.find({'stock': {'$lte': threshold}})
    
    products = []
    async for product_data in cursor:
        product = Product.from_dict(product_data)
        products.append(product.to_dict())
    
    return products 