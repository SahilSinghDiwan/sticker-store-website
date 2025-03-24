import os
from dotenv import load_dotenv
from flask import Flask
from app.config import get_config

def create_app(env=None):
    """Create and configure the Flask application.
    
    Args:
        env (str, optional): Environment name ('development', 'production', 'testing').
                           If None, uses FLASK_ENV from environment variables.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Load environment variables based on FLASK_ENV
    env = env or os.getenv('FLASK_ENV', 'development')
    load_dotenv(f'.env.{env}')
    
    app = Flask(__name__)
    
    # Load configuration based on environment
    config = get_config(env)
    app.config.from_object(config)
    
    # Initialize extensions
    from app import mongo, jwt, mail, cors, limiter
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.routes import auth_bp, products_bp, orders_bp, users_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)
    
    # Setup logging
    if not app.debug:
        # Configure production logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/sticker_shop.log', 
            maxBytes=10240, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Sticker Shop startup')
    
    return app

if __name__ == '__main__':
    # Get environment from command line or environment variable
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=env == 'development'
    )
