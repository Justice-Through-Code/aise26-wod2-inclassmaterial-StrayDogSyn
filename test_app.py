#!/usr/bin/env python3
"""
Simple test script to verify the Flask application works correctly.
"""

import sys
import tempfile
import os
import requests
import subprocess
import time
import threading

def test_app():
    """Test the Flask application."""
    print("=== Flask Application Verification Test ===\n")
    
    # Start the Flask app in background
    print("1. Starting Flask application...")
    
    # Set environment variables for testing
    os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-12345'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-12345'
    os.environ['DATABASE_URL'] = 'sqlite:///test_users.db'
    
    try:
        # Import and test the app
        from app import app, init_db
        
        # Initialize test database
        with app.app_context():
            init_db()
        
        print("✅ Flask app imported successfully")
        print("✅ Database initialized")
        
        # Test with test client
        with app.test_client() as client:
            print("\n2. Testing API endpoints...")
            
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
                data = response.get_json()
                print(f"   Status: {data.get('status')}")
            else:
                print("❌ Health endpoint failed")
                return False
            
            # Test user registration
            response = client.post('/users', json={
                'username': 'testuser123',
                'password': 'securepassword123'
            })
            if response.status_code == 201:
                print("✅ User registration working")
            else:
                print("❌ User registration failed")
                print(f"   Response: {response.get_json()}")
                return False
            
            # Test user login
            response = client.post('/login', json={
                'username': 'testuser123',
                'password': 'securepassword123'
            })
            if response.status_code == 200:
                print("✅ User login working")
                data = response.get_json()
                token = data.get('token')
                if token:
                    print("✅ JWT token generated")
                else:
                    print("❌ No JWT token in response")
                    return False
            else:
                print("❌ User login failed")
                return False
            
            # Test protected endpoint
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/users', headers=headers)
            if response.status_code == 200:
                print("✅ Protected endpoint working with JWT")
            else:
                print("❌ Protected endpoint failed")
                return False
            
            # Test security: invalid token
            headers = {'Authorization': 'Bearer invalid.token.here'}
            response = client.get('/users', headers=headers)
            if response.status_code == 401:
                print("✅ Invalid JWT token properly rejected")
            else:
                print("❌ Security issue: Invalid token accepted")
                return False
            
            print("\n3. Testing security measures...")
            
            # Test SQL injection protection
            response = client.post('/users', json={
                'username': "'; DROP TABLE users; --",
                'password': 'password123'
            })
            if response.status_code in [400, 422]:
                print("✅ SQL injection attempt blocked")
            else:
                print("❌ Security issue: SQL injection not prevented")
                return False
            
            # Test password validation
            response = client.post('/users', json={
                'username': 'validuser',
                'password': '123'  # Too short
            })
            if response.status_code == 400:
                print("✅ Password validation working")
            else:
                print("❌ Password validation failed")
                return False
        
        print("\n=== All Tests Passed! ===")
        print("✅ Flask application is working correctly")
        print("✅ Security measures are in place")
        print("✅ Authentication system functional")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        # Cleanup test database
        if os.path.exists('test_users.db'):
            os.remove('test_users.db')
        print("\n🧹 Cleanup completed")

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)