import pytest
import os
import tempfile
from app import app, init_db

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    # Create a temporary database file for testing
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['FLASK_SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret'
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    # Register and login a test user
    client.post('/users', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}