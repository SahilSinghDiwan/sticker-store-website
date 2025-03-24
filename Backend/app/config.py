import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Load the appropriate .env file based on FLASK_ENV
FLASK_ENV = os.getenv("FLASK_ENV", "development")
env_file = Path(f".env.{FLASK_ENV}")
load_dotenv(env_file)

class Config:
    """Base configuration."""
    
    # Flask
    FLASK_APP = os.getenv("FLASK_APP", "app")
    FLASK_ENV = FLASK_ENV
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    PORT = int(os.getenv("PORT", "5000"))
    
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "sticker_shop")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900"))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "604800"))
    
    # In-Memory Cache Settings (alternative to Redis)
    CACHE_TYPE = "SimpleCache"  # Built-in Flask-Caching option
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Rate Limiting (using in-memory storage)
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "100/15minute"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_CALLBACK_URL = os.getenv("GOOGLE_CALLBACK_URL")
    
    # Stripe (Optional)
    STRIPE_ENABLED = bool(os.getenv("STRIPE_SECRET_KEY"))
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    
    # Email (Optional)
    MAIL_ENABLED = bool(os.getenv("MAIL_USERNAME") and os.getenv("MAIL_PASSWORD"))
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    MONGODB_DB_NAME = "sticker_shop_dev"

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGODB_DB_NAME = "sticker_shop_test"
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Security headers
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
    REMEMBER_COOKIE_SECURE = os.getenv("REMEMBER_COOKIE_SECURE", "True") == "True"

# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

def get_config(env: str = None) -> Config:
    """Get configuration class based on environment."""
    env = env or FLASK_ENV
    config_class = config.get(env, config["default"])
    
    # Validate required environment variables
    required_vars = ["SECRET_KEY", "JWT_SECRET_KEY", "MONGO_URI"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return config_class

# Required environment variables
required_vars = [
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "MONGO_URI",
]

# Validate required environment variables
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 