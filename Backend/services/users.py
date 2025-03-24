from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
import bcrypt
from ..db.config import users_collection
from ..models.user import User

# Configuration
JWT_SECRET = "your-secret-key"  # Should be in environment variables
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

async def create_user(
    email: str,
    password: str,
    name: str,
    role: str = "customer"
) -> Dict[str, Any]:
    """Create a new user"""
    # Check if user already exists
    if await users_collection.find_one({'email': email}):
        raise ValueError("Email already registered")

    # Hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    user = {
        'email': email,
        'password': hashed_password,
        'name': name,
        'role': role,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'last_login': None,
        'active': True
    }

    result = await users_collection.insert_one(user)
    user['_id'] = result.inserted_id
    
    # Remove password from return value
    del user['password']
    return user

async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user and return JWT token"""
    user = await users_collection.find_one({'email': email})
    if not user:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return None

    # Update last login
    await users_collection.update_one(
        {'_id': user['_id']},
        {'$set': {'last_login': datetime.utcnow()}}
    )

    # Generate JWT token
    token = generate_jwt_token(str(user['_id']))

    # Remove password from return value
    del user['password']
    return {
        'user': user,
        'token': token
    }

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    user = await users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        del user['password']
        return user
    return None

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    user = await users_collection.find_one({'email': email})
    if user:
        del user['password']
        return user
    return None

async def update_user_profile(
    user_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Update user profile"""
    # Don't allow updating email or role through this function
    safe_updates = {
        k: v for k, v in updates.items()
        if k not in ['email', 'role', 'password']
    }
    
    if not safe_updates:
        return await get_user_by_id(user_id)

    safe_updates['updated_at'] = datetime.utcnow()
    
    await users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': safe_updates}
    )
    
    return await get_user_by_id(user_id)

async def change_password(
    user_id: str,
    old_password: str,
    new_password: str
) -> bool:
    """Change user password"""
    user = await users_collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return False

    if not bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
        return False

    # Hash new password
    salt = bcrypt.gensalt()
    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

    await users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {
            '$set': {
                'password': new_hashed_password,
                'updated_at': datetime.utcnow()
            }
        }
    )
    
    return True

async def deactivate_user(user_id: str) -> bool:
    """Deactivate user account"""
    result = await users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {
            '$set': {
                'active': False,
                'updated_at': datetime.utcnow()
            }
        }
    )
    return result.modified_count > 0

def generate_jwt_token(user_id: str) -> str:
    """Generate JWT token for user"""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': expiration
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def verify_jwt_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id if valid"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_admin_users() -> List[Dict[str, Any]]:
    """Get all admin users"""
    cursor = users_collection.find({'role': 'admin'})
    
    admin_users = []
    async for user in cursor:
        del user['password']
        admin_users.append(user)
    
    return admin_users 