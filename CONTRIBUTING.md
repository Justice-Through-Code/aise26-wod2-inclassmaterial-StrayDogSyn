# Contributing Guidelines

Thank you for your interest in contributing to the Secure User Management API! This document provides guidelines and best practices for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Security Requirements](#security-requirements)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git 2.25 or higher
- Virtual environment (venv or conda)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/secure-api.git
   cd secure-api
   ```

3. **Set up the development environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

5. **Configure environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env with your development values
   ```

## Development Workflow

### Branch Strategy

We use the **GitHub Flow** branching strategy:

1. **main branch**: Production-ready code
2. **feature branches**: New features or bug fixes
3. **hotfix branches**: Critical production fixes

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### Branch Naming Conventions

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `security/description` - Security improvements

## Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with the following specifics:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Import organization**: isort with Black profile
- **Docstrings**: Google style

### Code Formatting

All code is automatically formatted using:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import Optional, Dict, List

def create_user(username: str, password: str) -> Dict[str, str]:
    """Create a new user with the given credentials."""
    pass

def get_user_by_id(user_id: int) -> Optional[User]:
    """Retrieve user by ID, return None if not found."""
    pass
```

### Documentation Standards

- **Functions**: Include docstrings with parameters, return values, and examples
- **Classes**: Include class-level docstrings with usage examples  
- **Modules**: Include module-level docstrings explaining purpose
- **Comments**: Use sparingly, focus on "why" not "what"

Example:
```python
def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate user credentials and return JWT token.
    
    Args:
        username: User's username (3-255 characters)
        password: User's plaintext password (min 8 characters)
        
    Returns:
        JWT token string if authentication successful, None otherwise
        
    Raises:
        ValidationError: If input parameters are invalid
        DatabaseError: If database connection fails
        
    Example:
        >>> token = authenticate_user("john_doe", "securepass123")
        >>> if token:
        ...     print("Authentication successful")
    """
    pass
```

## Security Requirements

### Security-First Development

All contributions must adhere to security best practices:

#### Input Validation
```python
# Always validate and sanitize input
def validate_username(username: str) -> str:
    if not username or len(username.strip()) < 3:
        raise ValidationError("Username must be at least 3 characters")
    
    if len(username) > 255:
        raise ValidationError("Username too long")
        
    return username.strip()
```

#### SQL Injection Prevention
```python
# Always use parameterized queries
def get_user(username: str) -> Optional[User]:
    # GOOD ✅
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    # BAD ❌ - Never do this
    # cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

#### Password Security
```python
# Always use bcrypt for password hashing
import bcrypt

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

#### Secrets Management
```python
# Never hardcode secrets
# GOOD ✅
import os
DATABASE_URL = os.environ.get('DATABASE_URL')

# BAD ❌
# DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### Security Checklist

Before submitting code, ensure:

- [ ] No hardcoded secrets or credentials
- [ ] All inputs validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention measures implemented
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks implemented
- [ ] Sensitive data properly encrypted/hashed
- [ ] Error messages don't expose sensitive information
- [ ] Logging doesn't include sensitive data
- [ ] Dependencies are up-to-date and secure

## Testing Guidelines

### Test Structure

```text
tests/
├── unit/                 # Unit tests
│   ├── test_auth.py
│   ├── test_database.py
│   └── test_validation.py
├── integration/          # Integration tests
│   ├── test_api.py
│   └── test_workflows.py
├── security/            # Security tests
│   ├── test_injection.py
│   └── test_auth_bypass.py
└── conftest.py          # Test configuration
```

### Writing Tests

```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_user_creation_success(client):
    """Test successful user creation."""
    response = client.post('/users', json={
        'username': 'testuser',
        'password': 'securepass123'
    })
    assert response.status_code == 201
    assert 'User created successfully' in response.get_json()['message']

def test_user_creation_validation_error(client):
    """Test user creation with invalid input."""
    response = client.post('/users', json={
        'username': 'ab',  # Too short
        'password': '123'   # Too short
    })
    assert response.status_code == 400
```

### Security Testing

Include security-focused tests:

```python
def test_sql_injection_prevention(client):
    """Test that SQL injection attempts are blocked."""
    malicious_input = "'; DROP TABLE users; --"
    response = client.post('/users', json={
        'username': malicious_input,
        'password': 'password123'
    })
    # Should handle gracefully, not cause database error
    assert response.status_code in [400, 422]

def test_authentication_required(client):
    """Test that protected endpoints require authentication."""
    response = client.get('/users')
    assert response.status_code == 401
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/security/

# Run tests with verbose output
python -m pytest -v
```

## Pull Request Process

### Before Submitting

1. **Update your branch**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run quality checks**:
   ```bash
   # Format and lint
   black .
   isort .
   flake8 .
   
   # Run tests
   python -m pytest
   
   # Security scan
   bandit -r . -f txt
   ```

3. **Update documentation** if needed

### Pull Request Template

Your PR should include:

- **Clear title** describing the change
- **Description** of what was changed and why
- **Testing** information (what tests were added/updated)
- **Security** considerations
- **Breaking changes** (if any)

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Security review** for security-related changes
4. **Documentation review** if docs were updated

### Merge Requirements

- ✅ All CI/CD checks passing
- ✅ At least one approved review
- ✅ Up-to-date with main branch
- ✅ All conversations resolved

## Issue Reporting

### Bug Reports

Include:
- **Description**: Clear description of the issue
- **Steps to reproduce**: Detailed steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Screenshots**: If applicable

### Feature Requests

Include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Additional context**: Any other relevant information

### Security Issues

**DO NOT** report security vulnerabilities through public issues.

Instead:
- Email: [security@company.com](mailto:security@company.com)
- Include: Detailed description, steps to reproduce, potential impact
- We will respond within 24 hours

## Development Resources

### Helpful Commands

```bash
# Start development server
python app.py

# Run pre-commit hooks manually
pre-commit run --all-files

# Generate requirements.txt
pip freeze > requirements.txt

# Database migrations (if applicable)
flask db migrate -m "Description"
flask db upgrade
```

### IDE Configuration

#### VS Code Settings

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

## Questions and Support

- **General questions**: Open an issue with the "question" label
- **Development help**: Check existing issues or start a discussion
- **Security concerns**: Email [security@company.com](mailto:security@company.com)
- **Code review questions**: Comment on the relevant PR

Thank you for contributing to make this project more secure and robust!
