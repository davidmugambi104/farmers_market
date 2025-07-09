import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.logging import setup_logging
from config import config


limiter = Limiter(key_func=get_remote_address)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Setup logging
    setup_logging(app)  # Pass the app argument here
    
    # ... rest of the code ...
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.orders import orders_bp
    from routes.messages import messages_bp
    from routes.notifications import notifications_bp
    from routes.settings import settings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok'}), 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()