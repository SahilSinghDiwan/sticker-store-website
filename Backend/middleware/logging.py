import logging
import time
from flask import request, g
from functools import wraps
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app')

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Start timer
        start_time = time.time()
        
        # Log request
        request_data = {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'params': dict(request.args),
            'body': request.get_json(silent=True) if request.is_json else dict(request.form),
            'ip': request.remote_addr,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Remove sensitive information
        if request_data['headers'].get('Authorization'):
            request_data['headers']['Authorization'] = '[REDACTED]'
        if request_data.get('body', {}).get('password'):
            request_data['body']['password'] = '[REDACTED]'
            
        logger.info(f"Request: {json.dumps(request_data)}")
        
        try:
            # Execute request
            response = f(*args, **kwargs)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            response_data = {
                'status_code': response.status_code if hasattr(response, 'status_code') else 200,
                'duration': f"{duration:.3f}s",
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Response: {json.dumps(response_data)}")
            
            return response
            
        except Exception as e:
            # Log error
            error_data = {
                'error': str(e),
                'duration': f"{time.time() - start_time:.3f}s",
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.error(f"Error: {json.dumps(error_data)}")
            raise
            
    return decorated_function 