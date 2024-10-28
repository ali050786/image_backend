# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.cache import cache

def create_app():
    app = Flask(__name__)
    
    # Update CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })
    
    app.config.from_object(Config)
    cache.init_app(app)
    
    # Register blueprints
    from app.api.images import bp as images_bp
    from app.api.background import bp as background_bp
    
    app.register_blueprint(images_bp, url_prefix='/api/images')
    app.register_blueprint(background_bp, url_prefix='/api/background')
    
    return app