"""
GarudaRush Backend Application
Main Flask application entry point with authentication and traffic monitoring
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 24)))
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/GarudaRush')

# Enable CORS - Allow all origins for multi-device/network deployment
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize JWT
jwt = JWTManager(app)

# MongoDB Connection
try:
    mongo_client = MongoClient(app.config['MONGO_URI'], serverSelectionTimeoutMS=5000)
    # Test connection
    mongo_client.server_info()
    db = mongo_client[os.getenv('MONGO_DB_NAME', 'GarudaRush')]
    print("✓ MongoDB connection established")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    db = None

# Make db available to routes
app.config['DB'] = db

# Import routes
from routes.auth import auth_bp
from routes.traffic import traffic_bp
from routes.dashboard import dashboard_bp
from routes.alerts import alerts_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(traffic_bp, url_prefix='/api/traffic')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(alerts_bp, url_prefix='/api/alerts')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired', 'message': 'Please login again'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token', 'message': 'Token verification failed'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization required', 'message': 'Request does not contain an access token'}), 401

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'GarudaRush API',
        'version': '1.0.0',
        'database': 'connected' if db is not None else 'disconnected'
    }), 200

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'GarudaRush API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'traffic': '/api/traffic',
            'dashboard': '/api/dashboard',
            'alerts': '/api/alerts',
            'health': '/api/health'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print(f"""
    ╔═══════════════════════════════════════╗
    ║     🦅 GarudaRush Backend Started     ║
    ║                                       ║
    ║  Port: {port}                            ║
    ║  Debug: {str(debug):5}                        ║
    ║  MongoDB: {'Connected' if db is not None else 'Disconnected'}              ║
    ╚═══════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)