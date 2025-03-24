from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
import os
from .config import get_config

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()
cors = CORS()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()

def create_app(env=None):
    app = Flask(__name__)
    
    # Load configuration based on environment
    config = get_config(env)
    app.config.from_object(config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Initialize other extensions
    jwt.init_app(app)
    cors.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.orders import orders_bp
    from .routes.users import users_bp
    from .routes.uploads import uploads_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(uploads_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    return app
