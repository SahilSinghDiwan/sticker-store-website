from functools import wraps
from fastapi import HTTPException, Depends
from ..services.auth import get_current_user

async def admin_required(current_user = Depends(get_current_user)):
    """Middleware to check if the current user is an admin"""
    if not current_user or current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return current_user 