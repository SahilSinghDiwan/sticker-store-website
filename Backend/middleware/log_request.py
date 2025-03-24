from functools import wraps
from flask import request
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('request_logger')

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log request details
        request_data = {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'args': dict(request.args),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Remove sensitive information
        if 'Authorization' in request_data['headers']:
            request_data['headers']['Authorization'] = '[REDACTED]'
            
        logger.info(f"Request: {json.dumps(request_data)}")
        
        return f(*args, **kwargs)
    return decorated_function 