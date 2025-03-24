import logging
from logging.handlers import RotatingFileHandler
import traceback
from functools import wraps
from flask import jsonify
from typing import Any, Callable, Dict, Optional, Type, Union
import os

def setup_logger(app_name: str = 'sticker_shop') -> logging.Logger:
    """Configure application logger with rotating file handler and console output"""
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # File Handler - Rotating log files
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create logger instance
logger = setup_logger()

def handle_error(
    error: Exception,
    status_code: int = 500,
    custom_message: Optional[str] = None
) -> tuple[Dict[str, Any], int]:
    """Handle exceptions and return appropriate JSON response"""
    error_type = type(error).__name__
    error_details = str(error)
    
    # Log the full error with traceback
    logger.error(
        f"Error: {error_type} - {error_details}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )

    # Determine user-facing message
    message = custom_message or "An unexpected error occurred"
    
    # Include error details in development
    if os.getenv('FLASK_ENV') == 'development':
        return {
            'error': message,
            'type': error_type,
            'details': error_details,
            'traceback': traceback.format_exc()
        }, status_code
    
    # Production response
    return {
        'error': message
    }, status_code

def error_handler(func: Callable) -> Callable:
    """Decorator to handle exceptions in routes"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            return jsonify(handle_error(e, 400, str(e)))
        except KeyError as e:
            return jsonify(handle_error(e, 400, "Missing required field"))
        except Exception as e:
            return jsonify(handle_error(e))
    return wrapper

def validate_request_data(
    required_fields: list[str],
    data: Dict[str, Any]
) -> Optional[tuple[Dict[str, str], int]]:
    """Validate request data for required fields"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }, 400
    return None