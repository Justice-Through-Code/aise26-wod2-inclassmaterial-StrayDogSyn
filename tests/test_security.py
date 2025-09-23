"""
Security Tests
Tests specifically focused on security vulnerabilities and protections.
"""

def test_sql_injection_prevention_login(client):
    """Test that SQL injection attempts in login are blocked."""
    # Register a legitimate user first
    client.post('/users', json={
        'username': 'legitimate',
        'password': 'password123'
    })
    
    # Attempt SQL injection
    malicious_input = "'; DROP TABLE users; --"
    response = client.post('/login', json={
        'username': malicious_input,
        'password': 'password123'
    })
    
    # Should handle gracefully, not cause database error
    assert response.status_code == 401
    
    # Verify the legitimate user still exists (table wasn't dropped)
    response = client.post('/login', json={
        'username': 'legitimate',
        'password': 'password123'
    })
    assert response.status_code == 200

def test_sql_injection_prevention_registration(client):
    """Test that SQL injection attempts in registration are blocked."""
    malicious_input = "'; DROP TABLE users; --"
    response = client.post('/users', json={
        'username': malicious_input,
        'password': 'password123'
    })
    
    # Should handle gracefully, not cause database error
    assert response.status_code in [400, 422]

def test_password_hashing_verification(client):
    """Test that passwords are properly hashed."""
    import sqlite3
    
    # Register a user
    client.post('/users', json={
        'username': 'hashtest',
        'password': 'plaintextpassword'
    })
    
    # Check that password is not stored in plaintext
    conn = sqlite3.connect('users.db')
    cursor = conn.execute("SELECT password FROM users WHERE username = ?", ('hashtest',))
    stored_password = cursor.fetchone()[0]
    conn.close()
    
    # Password should be hashed (bcrypt hash starts with $2b$)
    assert stored_password != 'plaintextpassword'
    assert isinstance(stored_password, bytes)
    assert stored_password.startswith(b'$2b$')

def test_jwt_token_expiration(client):
    """Test that JWT tokens have expiration."""
    import jwt
    import os
    
    # Register and login
    client.post('/users', json={
        'username': 'tokentest',
        'password': 'password123'
    })
    
    response = client.post('/login', json={
        'username': 'tokentest',
        'password': 'password123'
    })
    
    token = response.get_json()['token']
    
    # Decode token and check expiration exists
    secret_key = os.environ.get('JWT_SECRET_KEY', 'test-jwt-secret')
    decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
    
    assert 'exp' in decoded
    assert 'iat' in decoded
    assert decoded['exp'] > decoded['iat']

def test_invalid_jwt_token(client):
    """Test that invalid JWT tokens are rejected."""
    headers = {'Authorization': 'Bearer invalid.token.here'}
    response = client.get('/users', headers=headers)
    assert response.status_code == 401

def test_missing_authorization_header(client):
    """Test that missing authorization header is handled."""
    response = client.get('/users')
    assert response.status_code == 401
    data = response.get_json()
    assert 'Token is missing' in data['message']

def test_input_validation_username_length(client):
    """Test username length validation."""
    # Username too short
    response = client.post('/users', json={
        'username': 'ab',
        'password': 'validpassword123'
    })
    assert response.status_code == 400
    
    # Username too long (over 255 characters)
    long_username = 'a' * 256
    response = client.post('/users', json={
        'username': long_username,
        'password': 'validpassword123'
    })
    assert response.status_code == 400

def test_password_strength_validation(client):
    """Test password strength requirements."""
    response = client.post('/users', json={
        'username': 'validuser',
        'password': '1234567'  # Less than 8 characters
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'Password must be at least 8 characters long' in data['error']

def test_no_sensitive_data_in_responses(client):
    """Test that sensitive data is not exposed in API responses."""
    # Register a user
    response = client.post('/users', json={
        'username': 'sensitivetest',
        'password': 'password123'
    })
    
    # Response should not contain password
    data = response.get_json()
    response_str = str(data)
    assert 'password123' not in response_str
    assert 'password' not in response_str.lower() or 'password' in ['password must be', 'password field']

def test_error_messages_no_information_disclosure(client):
    """Test that error messages don't disclose sensitive information."""
    # Try to login with non-existent user
    response = client.post('/login', json={
        'username': 'nonexistent',
        'password': 'password123'
    })
    
    # Should get generic error message, not specific information
    data = response.get_json()
    assert data['message'] == 'Invalid credentials'
    assert 'not found' not in data['message'].lower()
    assert 'does not exist' not in data['message'].lower()