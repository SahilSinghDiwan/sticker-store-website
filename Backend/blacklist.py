from datetime import datetime
from typing import Set, Dict
import threading

# In-memory storage for blacklisted tokens
# For production, use Redis or a database
_blacklisted_tokens: Set[str] = set()
_blacklist_lock = threading.Lock()

# Optional: Store expiration times to clean up old tokens
_token_expiry: Dict[str, datetime] = {}

def add_to_blacklist(token: str, expiry: datetime) -> None:
    """Add a token to the blacklist"""
    with _blacklist_lock:
        _blacklisted_tokens.add(token)
        _token_expiry[token] = expiry

def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted"""
    with _blacklist_lock:
        return token in _blacklisted_tokens

def remove_from_blacklist(token: str) -> None:
    """Remove a token from the blacklist"""
    with _blacklist_lock:
        _blacklisted_tokens.discard(token)
        _token_expiry.pop(token, None)

def cleanup_expired_tokens() -> None:
    """Remove expired tokens from the blacklist"""
    current_time = datetime.utcnow()
    with _blacklist_lock:
        expired_tokens = [
            token for token, expiry in _token_expiry.items()
            if expiry < current_time
        ]
        for token in expired_tokens:
            remove_from_blacklist(token)



