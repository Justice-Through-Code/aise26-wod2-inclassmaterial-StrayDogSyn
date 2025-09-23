# Secure User Management API

[![CI/CD Pipeline](https://github.com/yourusername/secure-api/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/secure-api/actions/workflows/ci.yml)
[![Security Rating](https://img.shields.io/badge/security-A+-green.svg)](https://github.com/yourusername/secure-api)

A professionally configured Flask API with comprehensive security measures, automated testing, and proper development workflows.

## 🔒 Security Features

- **Authentication & Authorization**: JWT-based authentication with secure token handling
- **Password Security**: bcrypt hashing with salt
- **Input Validation**: Comprehensive validation and sanitization
- **SQL Injection Prevention**: Parameterized queries throughout
- **Secrets Management**: Environment-based configuration
- **Security Scanning**: Automated vulnerability detection with Bandit
- **Pre-commit Hooks**: Automated security and quality checks

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/secure-api.git
   cd secure-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your actual values
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://127.0.0.1:5000`

## 📚 API Documentation

### Authentication

All endpoints except `/health`, `/users` (POST), and `/login` require a valid JWT token in the Authorization header:

```text
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Health Check
```http
GET /health
```

#### User Registration
```http
POST /users
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

#### User Login
```http
POST /login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

#### Get All Users (Authenticated)
```http
GET /users
Authorization: Bearer <token>
```

#### Get User Profile (Authenticated)
```http
GET /profile
Authorization: Bearer <token>
```

## 🛡️ Security Measures Implemented

### Fixed Vulnerabilities from Original Code

1. **Hardcoded Secrets** → Environment variables and secure key generation
2. **SQL Injection** → Parameterized queries throughout
3. **Weak Password Hashing** → bcrypt with proper salt
4. **Missing Input Validation** → Comprehensive validation and sanitization
5. **Insecure Logging** → Structured logging without sensitive data
6. **Debug Mode in Production** → Environment-controlled debug settings
7. **Generic Error Messages** → Proper error handling without information disclosure
8. **Missing Authentication** → JWT-based authentication system

### Additional Security Enhancements

- Session management with secure cookies
- Rate limiting considerations (ready for implementation)
- CORS protection (configurable)
- Content Security Policy headers
- Automated security scanning in CI/CD
- Dependency vulnerability monitoring

## 🔧 Development Workflow

### Branch Protection Rules

Our main branch is protected with the following rules:
- Require pull request reviews (minimum 1)
- Dismiss stale PR approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in restrictions

### Pre-commit Hooks

Automatically run on every commit:
- **Security**: Bandit security linting, secrets detection
- **Code Quality**: Black formatting, isort import sorting, flake8 linting
- **General**: Trailing whitespace, file endings, YAML/JSON validation

### CI/CD Pipeline

Our GitHub Actions pipeline includes:
- Security scanning (Bandit, Safety)
- Code quality checks (Black, isort, flake8)
- Automated testing
- Dependency vulnerability scanning

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run security tests only
python -m pytest tests/test_security.py
```

## 📋 Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests and pre-commit hooks
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **Type hints** where appropriate

## 🚨 Security Reporting

If you discover a security vulnerability, please send an email to [security@yourcompany.com](mailto:security@yourcompany.com). All security vulnerabilities will be promptly addressed.

**Please do not report security vulnerabilities through public GitHub issues.**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Flask team for the excellent web framework
- OWASP for security best practices
- Pre-commit team for development workflow tools

## 📞 Support

- Create an issue for bug reports or feature requests
- Check our [documentation](docs/) for detailed guides
- Contact the team at [support@yourcompany.com](mailto:support@yourcompany.com)

---

**⚠️ Important**: This API was developed as part of a security-focused assignment, transforming intentionally vulnerable code into a secure, professionally configured application.
