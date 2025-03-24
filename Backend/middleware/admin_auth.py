from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from ..db import db
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'message': 'Missing authorization header'}), 401
        
        try:
            if 'Bearer' in auth_header:
                # JWT Token authentication
                token = auth_header.split(" ")[1]
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                
                if not data.get('is_admin'):
                    return jsonify({'message': 'Admin privileges required'}), 403
                    
            elif 'Basic' in auth_header:
                # Basic authentication for development/testing
                credentials = auth_header.split(" ")[1]
                username, password = jwt.decode(credentials.encode(), options={"verify_signature": False}).split(':')
                
                admin_user = db.users.find_one({
                    'email': username,
                    'is_admin': True
                })
                
                if not admin_user or not check_password_hash(admin_user['password'], password):
                    return jsonify({'message': 'Invalid admin credentials'}), 401
            else:
                return jsonify({'message': 'Invalid authorization header'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': f'Authentication error: {str(e)}'}), 401
            
        return f(*args, **kwargs)
    return decorated

def create_admin_token(user_id: str) -> str:
    """Create a JWT token for admin authentication"""
    token = jwt.encode(
        {
            'user_id': str(user_id),
            'is_admin': True,
            'exp': datetime.utcnow() + timedelta(days=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token 