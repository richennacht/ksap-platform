"""
KSAP E-commerce Management Platform - Main Flask Application

This module creates and configures the Flask application with Supabase integration.
Following Flask best practices from: https://flask.palletsprojects.com/en/3.0.x/patterns/

References:
- Flask Documentation: https://flask.palletsprojects.com/
- Flask-CORS: https://flask-cors.readthedocs.io/
- Supabase Python: https://supabase.com/docs/reference/python/introduction
"""

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import logging

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """
    Application factory pattern for creating Flask app.
    Reference: https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configuration following Flask best practices
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Let Supabase handle token expiration
    
    # Supabase configuration
    app.config['SUPABASE_URL'] = os.environ.get('SUPABASE_URL', '')
    app.config['SUPABASE_ANON_KEY'] = os.environ.get('SUPABASE_ANON_KEY', '')
    app.config['SUPABASE_SERVICE_KEY'] = os.environ.get('SUPABASE_SERVICE_KEY', '')
    
    # Initialize extensions following Flask patterns
    # CORS configuration: https://flask-cors.readthedocs.io/en/latest/
    CORS(app, 
         origins="*",  # Allow all origins for development
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])
    
    # JWT Manager: https://flask-jwt-extended.readthedocs.io/
    jwt = JWTManager(app)
    
    # Test Supabase connection on startup
    try:
        from src.database import supabase_client
        if supabase_client.test_connection():
            logger.info("✅ Supabase connection successful")
        else:
            logger.warning("❌ Supabase connection failed")
    except Exception as e:
        logger.error(f"❌ Supabase connection error: {e}")
    
    # Register blueprints following Flask patterns
    # Reference: https://flask.palletsprojects.com/en/3.0.x/blueprints/
    try:
        from src.routes.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/v1/users')
        logger.info("✅ Registered user blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import user blueprint: {e}")
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """
        Health check endpoint for monitoring and load balancers.
        Returns JSON with service status and dependencies.
        """
        try:
            from src.database import supabase_client
            supabase_connected = supabase_client.test_connection()
            
            health_status = {
                'status': 'healthy' if supabase_connected else 'degraded',
                'version': '1.0.0',
                'services': {
                    'supabase': 'connected' if supabase_connected else 'disconnected',
                    'flask': 'running'
                },
                'environment': os.environ.get('FLASK_ENV', 'production')
            }
            
            status_code = 200 if supabase_connected else 503
            return jsonify(health_status), status_code
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'version': '1.0.0'
            }), 503
    
    # Root endpoint with API documentation
    @app.route('/')
    def root():
        """
        Root endpoint providing API information and available endpoints.
        """
        return jsonify({
            'message': 'KSAP E-commerce Management Platform API',
            'version': '1.0.0',
            'status': 'running',
            'documentation': {
                'framework_references': '/docs/FRAMEWORK_REFERENCES.md',
                'api_docs': '/docs/api/',
                'architecture': '/docs/KSAP_Architecture_Design.md'
            },
            'endpoints': {
                'health': '/health',
                'users': '/api/v1/users',
                'stores': '/api/v1/stores',
                'products': '/api/v1/products',
                'orders': '/api/v1/orders',
                'analytics': '/api/v1/analytics',
                'social': '/api/v1/social'
            },
            'technologies': {
                'backend': 'Flask 3.1.1',
                'database': 'Supabase (PostgreSQL)',
                'authentication': 'Supabase Auth',
                'deployment': 'Gunicorn WSGI'
            }
        })
    
    # Error handlers following Flask patterns
    # Reference: https://flask.palletsprojects.com/en/3.0.x/errorhandling/
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors with consistent JSON response"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found',
                'status': 404
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors with consistent JSON response"""
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred',
                'status': 500
            }
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors with consistent JSON response"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'BAD_REQUEST',
                'message': 'The request was invalid or malformed',
                'status': 400
            }
        }), 400
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired JWT tokens"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'TOKEN_EXPIRED',
                'message': 'The JWT token has expired'
            }
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid JWT tokens"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_TOKEN',
                'message': 'The JWT token is invalid'
            }
        }), 401
    
    return app

# Create app instance using factory pattern
app = create_app()

if __name__ == '__main__':
    """
    Development server configuration.
    For production, use Gunicorn: https://docs.gunicorn.org/
    """
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting KSAP API server on port {port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"🌐 CORS enabled for all origins")
    logger.info(f"📚 Framework documentation: /docs/FRAMEWORK_REFERENCES.md")
    
    # Run with host='0.0.0.0' to allow external connections
    # Reference: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
