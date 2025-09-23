# Secure Python API - Professional Implementation
# Fixed all security vulnerabilities from starter code

import os
import secrets
import logging
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify, session
import sqlite3
import bcrypt
import jwt
from werkzeug.exceptions import BadRequest

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security Fix: Use environment variables and generate secure keys
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))

# Security configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        return sqlite3.connect('users.db')
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def validate_input(data, required_fields):
    """Validate input data and required fields"""
    if not data:
        raise BadRequest("No JSON data provided")
    
    for field in required_fields:
        if field not in data or not data[field]:
            raise BadRequest(f"Missing required field: {field}")
        
        # Security Fix: Input validation
        field_value = str(data[field])
        if len(field_value) > 255:
            raise BadRequest(f"Field {field} exceeds maximum length")
        
        # Security Fix: Check for SQL injection patterns
        suspicious_patterns = [
            "drop table", "delete from", "update ", "insert into",
            "truncate", "alter table", "create table", "--", ";",
            "union select", "or 1=1", "' or", "\" or"
        ]
        
        field_lower = field_value.lower()
        for pattern in suspicious_patterns:
            if pattern in field_lower:
                raise BadRequest(f"Invalid characters detected in {field}")
    
    return True

def generate_token(user_id):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route('/health')
def health_check():
    """Health check endpoint - Security Fix: No sensitive information exposed"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    """Get all users - requires authentication"""
    try:
        conn = get_db_connection()
        # Security Fix: Use parameterized queries, don't expose sensitive data
        users = conn.execute('SELECT id, username, created_at FROM users').fetchall()
        conn.close()
        
        return jsonify({
            "users": [
                {"id": u[0], "username": u[1], "created_at": u[2]} 
                for u in users
            ]
        })
    except sqlite3.Error as e:
        logger.error(f"Database error in get_users: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user with secure password handling"""
    try:
        data = request.get_json()
        validate_input(data, ['username', 'password'])
        
        username = data.get('username').strip()
        password = data.get('password')
        
        # Security Fix: Password strength validation
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        # Security Fix: Use bcrypt for secure password hashing
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        conn = get_db_connection()
        
        # Security Fix: Use parameterized queries to prevent SQL injection
        try:
            conn.execute(
                "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                (username, hashed_password, datetime.utcnow().isoformat())
            )
            conn.commit()
            
            # Security Fix: Secure logging - no sensitive information
            logger.info(f"User created: {username}")
            
            return jsonify({"message": "User created successfully", "username": username}), 201
            
        except sqlite3.IntegrityError:
            return jsonify({"error": "Username already exists"}), 409
        finally:
            conn.close()
            
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/login', methods=['POST'])
def login():
    """User login with secure authentication"""
    try:
        data = request.get_json()
        validate_input(data, ['username', 'password'])
        
        username = data.get('username').strip()
        password = data.get('password')
        
        conn = get_db_connection()
        
        # Security Fix: Use parameterized queries
        user = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?", 
            (username,)
        ).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            # Generate JWT token
            token = generate_token(user[0])
            
            # Security Fix: Secure logging - no sensitive information
            logger.info(f"Successful login for user: {username}")
            
            return jsonify({
                "message": "Login successful",
                "token": token,
                "user_id": user[0]
            })
        
        # Security Fix: Generic error message to prevent user enumeration
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({"message": "Invalid credentials"}), 401
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    """Get current user's profile"""
    try:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?", 
            (current_user_id,)
        ).fetchone()
        conn.close()
        
        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "created_at": user[2]
            })
        
        return jsonify({"error": "User not found"}), 404
        
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

def init_db():
    """Initialize database with proper schema"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            created_at TEXT NOT NULL,
            CONSTRAINT username_length CHECK (length(username) <= 255)
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

if __name__ == '__main__':
    init_db()
    
    # Security Fix: Disable debug mode in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)