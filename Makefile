.PHONY: install test lint format security clean run setup

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Set up development environment
setup: install
	pre-commit install
	cp .env.template .env
	@echo "Development environment setup complete!"
	@echo "Please edit .env with your configuration values."

# Run the application
run:
	python app.py

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-cov:
	python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# Format code
format:
	black .
	isort .

# Lint code
lint:
	flake8 .
	black --check .
	isort --check-only .

# Security checks
security:
	bandit -r . -f txt -ll
	safety check

# Run all quality checks
quality: lint security test

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f *.db

# Help
help:
	@echo "Available commands:"
	@echo "  setup     - Set up development environment"
	@echo "  install   - Install dependencies"
	@echo "  run       - Run the application"
	@echo "  test      - Run tests"
	@echo "  test-cov  - Run tests with coverage"
	@echo "  format    - Format code with black and isort"
	@echo "  lint      - Run linting checks"
	@echo "  security  - Run security scans"
	@echo "  quality   - Run all quality checks"
	@echo "  clean     - Clean temporary files"