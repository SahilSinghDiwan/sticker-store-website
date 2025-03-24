from functools import wraps
from flask import request, jsonify
import redis
import time
from datetime import datetime

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class RateLimitExceeded(Exception):
    pass

def rate_limit(requests: int, window: int):
    """
    Rate limiting decorator
    requests: number of requests allowed
    window: time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            ip = request.remote_addr
            # Create a key for the IP and endpoint
            key = f"rate_limit:{ip}:{request.endpoint}"
            
            try:
                # Get current requests count
                requests_count = int(redis_client.get(key) or 0)
                
                if requests_count >= requests:
                    raise RateLimitExceeded
                
                # Increment requests count
                pipe = redis_client.pipeline()
                pipe.incr(key)
                pipe.expire(key, window)
                pipe.execute()
                
                return f(*args, **kwargs)
                
            except RateLimitExceeded:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Please wait {window} seconds before trying again'
                }), 429
            except redis.RedisError:
                # If Redis is down, allow the request but log the error
                print(f"Redis error at {datetime.utcnow()}: Rate limiting unavailable")
                return f(*args, **kwargs)
                
        return decorated_function
    return decorator 