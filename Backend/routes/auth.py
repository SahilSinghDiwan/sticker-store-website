from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict
from ..services.auth import create_user, request_password_reset, reset_password

auth = Blueprint('auth', __name__)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if db.users.find_one({'email': data['email']}):
            return jsonify({'error': 'Email already registered'}), 400
            
        # Hash password
        data['password'] = generate_password_hash(data['password'])
        
        # Insert user
        db.users.insert_one(data)
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = db.users.find_one({'email': data['email']})
        
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
            
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user = db.users.find_one({'_id': user_id}, {'password': 0})
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.post("/forgot-password")
async def forgot_password(data: PasswordResetRequest) -> Dict:
    """Request password reset email"""
    try:
        await request_password_reset(data.email)
        return {"message": "If an account exists with this email, a password reset link will be sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process request")

@auth.post("/reset-password")
async def reset_password_endpoint(data: PasswordReset) -> Dict:
    """Reset password using reset token"""
    try:
        await reset_password(data.token, data.new_password)
        return {"message": "Password reset successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to reset password") 