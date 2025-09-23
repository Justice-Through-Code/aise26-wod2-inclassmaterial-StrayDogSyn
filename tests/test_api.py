"""
API Integration Tests
Tests for the complete API functionality including authentication flows.
"""

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data

def test_user_registration_success(client):
    """Test successful user registration."""
    response = client.post('/users', json={
        'username': 'newuser',
        'password': 'securepass123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'
    assert data['username'] == 'newuser'

def test_user_registration_validation_error(client):
    """Test user registration with invalid input."""
    response = client.post('/users', json={
        'username': 'ab',  # Too short
        'password': '123'   # Too short
    })
    assert response.status_code == 400

def test_user_login_success(client):
    """Test successful user login."""
    # First register a user
    client.post('/users', json={
        'username': 'loginuser',
        'password': 'loginpass123'
    })
    
    # Then login
    response = client.post('/login', json={
        'username': 'loginuser',
        'password': 'loginpass123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert 'token' in data
    assert 'user_id' in data

def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/login', json={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['message'] == 'Invalid credentials'

def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without authentication."""
    response = client.get('/users')
    assert response.status_code == 401
    data = response.get_json()
    assert 'Token is missing' in data['message']

def test_protected_endpoint_with_valid_token(client, auth_headers):
    """Test accessing protected endpoint with valid token."""
    response = client.get('/users', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data

def test_user_profile_endpoint(client, auth_headers):
    """Test user profile endpoint."""
    response = client.get('/profile', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'username' in data
    assert 'created_at' in data