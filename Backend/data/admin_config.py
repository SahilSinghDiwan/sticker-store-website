import os
from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash

# You should move these to environment variables in production
ADMIN_USERNAME = "admin"
# This is a hashed version of "admin123" - you should change this in production
ADMIN_PASSWORD_HASH = "pbkdf2:sha256:600000$6qcN5mhs$4c1bd72c6b97db0c2c163c1b5a1e54f8f0e3c2fbc1f645f6c40cf6c3b5b7f9c"

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization

        if not auth or not check_admin_credentials(auth.username, auth.password):
            return jsonify({
                "message": "Unauthorized access",
                "error": "Invalid admin credentials"
            }), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
            
        return f(*args, **kwargs)
    return decorated_function

def check_admin_credentials(username, password):
    return username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password) 