from flask import jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from blacklist import add_to_blacklist
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable

from db import users_collection
from .services.users import get_user_by_email, create_user, get_user_by_id
from .blacklist import is_token_blacklisted
from dotenv import load_dotenv

load_dotenv()



def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def register_user(firstName, lastName, email, password, phoneNumber, provider=None, providerId=None):
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hash_password(password)
    users_collection.insert_one({"username": email, "email": email, "password": hashed_password, "firstName": firstName, "lastName": lastName, "phoneNumber": phoneNumber, "provider": provider, "providerId": providerId})
    return jsonify({"message": "User registered successfully"}), 201

def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token, "message": "Login successful"}), 200

@jwt_required()
def logout_user():
    jti = get_jwt()["jti"]
    add_to_blacklist(jti)
    return jsonify({"message": "Successfully logged out"}), 200

def generate_jwt_token(user_id: str) -> str:
    """Generate a JWT token for a user"""
    expiration = datetime.utcnow() + timedelta(hours=os.getenv("JWT_EXPIRATION_HOURS"))
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': expiration
        },
        os.getenv("JWT_SECRET"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )

def verify_jwt_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id if valid"""
    try:
        if is_token_blacklisted(token):
            return None
            
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Google OAuth token and return user info"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None

        return {
            'email': idinfo['email'],
            'name': idinfo['name'],
            'picture': idinfo.get('picture')
        }
    except ValueError:
        return None

def login_required(f: Callable) -> Callable:
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Missing token'}), 401

        user_id = verify_jwt_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401

        return await f(*args, **kwargs)
    return decorated_function

def admin_required(f: Callable) -> Callable:
    """Decorator to protect routes that require admin access"""
    @wraps(f)
    @login_required
    async def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]
        user_id = verify_jwt_token(token)
        
        # Get user from database and check role
        user = await get_user_by_id(user_id)
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403

        return await f(*args, **kwargs)
    return decorated_function

async def handle_google_auth(token: str) -> Optional[Dict[str, Any]]:
    """Handle Google OAuth authentication flow"""
    user_info = await verify_google_token(token)
    if not user_info:
        return None

    # Check if user exists
    user = await get_user_by_email(user_info['email'])
    
    if not user:
        # Create new user from Google data
        user = await create_user(
            email=user_info['email'],
            name=user_info['name'],
            password=None,  # Google OAuth users don't have password
            role='customer'
        )

    # Generate JWT token
    token = generate_jwt_token(str(user['_id']))
    
    return {
        'user': user,
        'token': token
    }