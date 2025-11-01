.PHONY: help setup install train test serve mlflow docker-build docker-run clean lint format verify

# Default target
help:
	@echo "MLOps Demo - Available Commands"
	@echo "================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup         - Create virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make verify        - Verify setup is correct"
	@echo ""
	@echo "Development Commands:"
	@echo "  make train         - Train the model"
	@echo "  make test          - Run tests"
	@echo "  make serve         - Start FastAPI service"
	@echo "  make mlflow        - Start MLflow UI"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-test   - Test Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove generated files"
	@echo "  make clean-all     - Remove all (including venv)"

# Setup
setup:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "✓ Virtual environment created"
	@echo ""
	@echo "Activate with: source venv/bin/activate"

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

verify:
	@echo "Verifying setup..."
	chmod +x verify_setup.sh
	./verify_setup.sh

# Training and Inference
train:
	@echo "Training model..."
	python src/train.py

test:
	@echo "Running tests..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

serve:
	@echo "Starting FastAPI service..."
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

mlflow:
	@echo "Starting MLflow UI..."
	@echo "Open http://localhost:5000 in your browser"
	mlflow ui

# Code Quality
lint:
	@echo "Running linters..."
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503 || true
	@echo "Checking types..."
	mypy src/ --ignore-missing-imports || true

format:
	@echo "Formatting code..."
	black src/ tests/
	@echo "✓ Code formatted"

# Docker
docker-build:
	@echo "Building Docker image..."
	docker build -t mlops-demo:latest .
	@echo "✓ Docker image built"

docker-run:
	@echo "Running Docker container..."
	docker run -d -p 8000:8000 --name mlops-demo mlops-demo:latest
	@echo "✓ Container started"
	@echo "API available at: http://localhost:8000"
	@echo "Stop with: docker stop mlops-demo"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop mlops-demo || true
	docker rm mlops-demo || true
	@echo "✓ Container stopped"

docker-test:
	@echo "Testing Docker container..."
	docker run -d -p 8000:8000 --name mlops-demo-test mlops-demo:latest
	@echo "Waiting for service to start..."
	sleep 5
	@echo "Testing health endpoint..."
	curl -f http://localhost:8000/health
	@echo ""
	@echo "Testing predict endpoint..."
	curl -X POST http://localhost:8000/predict \
		-H "Content-Type: application/json" \
		-d '{"features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}'
	@echo ""
	docker stop mlops-demo-test
	docker rm mlops-demo-test
	@echo "✓ Docker tests passed"

docker-shell:
	@echo "Opening shell in Docker container..."
	docker run -it --rm mlops-demo:latest /bin/bash

# Cleanup
clean:
	@echo "Cleaning generated files..."
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Cleaned"

clean-mlflow:
	@echo "Cleaning MLflow artifacts..."
	rm -rf mlruns mlartifacts
	@echo "✓ MLflow artifacts removed"

clean-all: clean clean-mlflow
	@echo "Removing virtual environment..."
	rm -rf venv
	@echo "Removing Docker images..."
	docker rmi mlops-demo:latest 2>/dev/null || true
	@echo "✓ Everything cleaned"

# Quick start
quickstart:
	@echo "Running quick start..."
	chmod +x quickstart.sh
	./quickstart.sh

# CI/CD simulation
ci:
	@echo "Simulating CI/CD pipeline..."
	@echo ""
	@echo "→ Step 1: Linting"
	@make lint
	@echo ""
	@echo "→ Step 2: Training"
	@make train
	@echo ""
	@echo "→ Step 3: Testing"
	@make test
	@echo ""
	@echo "→ Step 4: Docker Build"
	@make docker-build
	@echo ""
	@echo "✓ CI pipeline complete"
