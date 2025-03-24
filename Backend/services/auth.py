import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
from .email import send_password_reset_email, send_welcome_email
from ..db import users_collection

JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
RESET_TOKEN_EXPIRY = 3600  # 1 hour in seconds

async def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    """Create a new user account"""
    # Check if user already exists
    existing_user = await users_collection.find_one({'email': email})
    if existing_user:
        raise ValueError('User already exists')
    
    # Hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    
    # Create user document
    user = {
        'email': email,
        'password': hashed_password,
        'name': name,
        'created_at': datetime.utcnow(),
        'reset_token': None,
        'reset_token_expires': None
    }
    
    # Insert into database
    result = await users_collection.insert_one(user)
    user['_id'] = result.inserted_id
    
    # Send welcome email
    await send_welcome_email(user)
    
    # Remove password from return value
    del user['password']
    return user

async def request_password_reset(email: str) -> None:
    """Generate password reset token and send reset email"""
    user = await users_collection.find_one({'email': email})
    if not user:
        # Don't reveal if user exists
        return
    
    # Generate reset token
    reset_token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(seconds=RESET_TOKEN_EXPIRY)
    }, JWT_SECRET)
    
    # Store reset token and expiry
    await users_collection.update_one(
        {'_id': user['_id']},
        {
            '$set': {
                'reset_token': reset_token,
                'reset_token_expires': datetime.utcnow() + timedelta(seconds=RESET_TOKEN_EXPIRY)
            }
        }
    )
    
    # Send reset email
    await send_password_reset_email(user, reset_token)

async def reset_password(token: str, new_password: str) -> None:
    """Reset user password using reset token"""
    try:
        # Verify token
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Find user with valid reset token
        user = await users_collection.find_one({
            '_id': user_id,
            'reset_token': token,
            'reset_token_expires': {'$gt': datetime.utcnow()}
        })
        
        if not user:
            raise ValueError('Invalid or expired reset token')
        
        # Hash new password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode(), salt)
        
        # Update password and clear reset token
        await users_collection.update_one(
            {'_id': user['_id']},
            {
                '$set': {'password': hashed_password},
                '$unset': {
                    'reset_token': '',
                    'reset_token_expires': ''
                }
            }
        )
        
    except jwt.ExpiredSignatureError:
        raise ValueError('Reset token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid reset token') 