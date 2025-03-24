from flask_cors import CORS
from typing import Dict, List
import os

def setup_cors(app) -> None:
    """Configure CORS for different environments"""
    env = os.getenv('FLASK_ENV', 'development')
    
    cors_config: Dict[str, Dict] = {
        'development': {
            'origins': [
                'http://localhost:3000',  # React dev server
                'http://127.0.0.1:3000',
                'http://localhost:5000'   # Flask dev server
            ],
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization'],
            'expose_headers': ['Content-Range', 'X-Total-Count'],
            'supports_credentials': True
        },
        'production': {
            'origins': [
                os.getenv('FRONTEND_URL', 'https://yourdomain.com'),
                os.getenv('API_URL', 'https://api.yourdomain.com')
            ],
            'methods': ['GET', 'POST', 'PUT', 'DELETE'],
            'allow_headers': ['Content-Type', 'Authorization'],
            'expose_headers': ['Content-Range', 'X-Total-Count'],
            'supports_credentials': True
        }
    }
    
    CORS(app, **cors_config[env]) 