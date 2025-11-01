# MLOps Workshop - Quick Reference Cheat Sheet

## 🚀 Quick Commands

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
./verify_setup.sh
# OR
make verify
```

### Training & Experiments
```bash
# Train model
python src/train.py
# OR
make train

# Start MLflow UI
mlflow ui
# Open: http://localhost:5000
```

### API Service
```bash
# Start development server
uvicorn src.app:app --reload --port 8000
# OR
make serve

# View interactive docs
# Open: http://localhost:8000/docs
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_infer_contract.py::TestHealthEndpoint -v
```

### Docker
```bash
# Build image
docker build -t mlops-demo .

# Run container
docker run -p 8000:8000 mlops-demo

# Run in background
docker run -d -p 8000:8000 --name mlops-demo mlops-demo

# Stop container
docker stop mlops-demo

# View logs
docker logs mlops-demo

# Remove container
docker rm mlops-demo
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### GET `/`
Service information
```bash
curl http://localhost:8000/
```

#### GET `/health`
Health check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1"
}
```

#### GET `/contract`
API contract schemas
```bash
curl http://localhost:8000/contract
```

#### POST `/predict`
Make prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    }
  }'
```

Response:
```json
{
  "prediction": 0,
  "prediction_label": "setosa",
  "confidence": 0.95,
  "model_version": "1"
}
```

---

## 🧪 Example Predictions

### Setosa (Class 0)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}'
```

### Versicolor (Class 1)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": 6.0, "sepal_width": 2.7, "petal_length": 5.1, "petal_width": 1.6}}'
```

### Virginica (Class 2)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": 7.2, "sepal_width": 3.0, "petal_length": 5.8, "petal_width": 1.6}}'
```

---

## 📊 MLflow Commands

```bash
# Start UI
mlflow ui

# Start on different port
mlflow ui --port 5001

# View specific experiment
mlflow experiments list
mlflow runs list --experiment-id 0

# Search runs
mlflow runs list --experiment-name iris-classification

# Export run
mlflow artifacts download --run-id <RUN_ID>
```

---

## 🐳 Docker Commands Reference

### Build
```bash
# Basic build
docker build -t mlops-demo .

# Build with tag
docker build -t mlops-demo:v1.0 .

# Build with no cache
docker build --no-cache -t mlops-demo .
```

### Run
```bash
# Run interactively
docker run -it -p 8000:8000 mlops-demo

# Run in background
docker run -d -p 8000:8000 --name mlops-demo mlops-demo

# Run with environment variables
docker run -p 8000:8000 -e MLFLOW_TRACKING_URI=mlruns mlops-demo

# Run with volume mount
docker run -p 8000:8000 -v $(pwd)/mlruns:/app/mlruns mlops-demo
```

### Manage
```bash
# List containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop mlops-demo

# Remove container
docker rm mlops-demo

# View logs
docker logs mlops-demo

# Follow logs
docker logs -f mlops-demo

# Execute command in container
docker exec -it mlops-demo /bin/bash

# Inspect container
docker inspect mlops-demo

# Check container health
docker inspect --format='{{.State.Health.Status}}' mlops-demo
```

### Images
```bash
# List images
docker images

# Remove image
docker rmi mlops-demo

# Tag image
docker tag mlops-demo:latest mlops-demo:v1.0

# Push to registry
docker push username/mlops-demo:latest

# Save image to file
docker save mlops-demo > mlops-demo.tar

# Load image from file
docker load < mlops-demo.tar
```

---

## 🧪 Pytest Commands

```bash
# Run all tests
pytest tests/

# Verbose output
pytest tests/ -v

# Very verbose (show print statements)
pytest tests/ -vv -s

# Run specific test file
pytest tests/test_infer_contract.py

# Run specific test class
pytest tests/test_infer_contract.py::TestHealthEndpoint

# Run specific test method
pytest tests/test_infer_contract.py::TestHealthEndpoint::test_health_check_status_code

# Run tests matching pattern
pytest tests/ -k "health"

# Stop on first failure
pytest tests/ -x

# Show coverage
pytest tests/ --cov=src

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html

# Show slowest tests
pytest tests/ --durations=10

# Run in parallel (requires pytest-xdist)
pytest tests/ -n auto
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# OR
netstat -tulpn | grep 8000

# Kill process
kill -9 <PID>
```

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv

# Create new environment
python -m venv venv

# Activate
source venv/bin/activate
```

### MLflow Issues
```bash
# Clean MLflow artifacts
rm -rf mlruns mlartifacts

# Retrain model
python src/train.py

# Check MLflow tracking URI
echo $MLFLOW_TRACKING_URI
```

### Docker Issues
```bash
# Check Docker status
docker info

# Start Docker daemon (Linux)
sudo systemctl start docker

# Prune unused resources
docker system prune -a

# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a
```

### Permission Issues
```bash
# Make scripts executable
chmod +x quickstart.sh verify_setup.sh

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📁 Project Structure Quick Reference

```
mlops-demo/
├── data/raw/iris.csv          # Dataset
├── src/
│   ├── train.py               # Training script
│   ├── app.py                 # FastAPI service
│   └── infer_schema.py        # API contracts
├── tests/
│   └── test_infer_contract.py # API tests
├── requirements.txt           # Dependencies
├── Dockerfile                 # Container definition
├── Makefile                   # Common commands
├── quickstart.sh              # Auto-setup script
├── verify_setup.sh            # Verification script
└── README.md                  # Documentation
```

---

## 🎯 Workshop Flow

1. **Setup** → `make setup && make install`
2. **Train** → `make train`
3. **Explore** → `make mlflow` (view experiments)
4. **Serve** → `make serve` (start API)
5. **Test** → `make test` (run tests)
6. **Containerize** → `make docker-build`
7. **Deploy** → `make docker-run`

---

## 💡 Tips & Tricks

### View API Docs
- Interactive: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Watch Logs
```bash
# API logs (development)
uvicorn src.app:app --reload --log-level debug

# Docker logs (follow)
docker logs -f mlops-demo
```

### Quick Test Cycle
```bash
# Terminal 1: Auto-reload server
uvicorn src.app:app --reload

# Terminal 2: Watch tests
pytest-watch tests/
```

### Environment Variables
```bash
# Set MLflow tracking URI
export MLFLOW_TRACKING_URI=mlruns

# Set API port
export PORT=8000

# Load from .env file
export $(cat .env | xargs)
```

---

## 🚨 Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `Address already in use` | Kill process: `lsof -i :8000` then `kill -9 <PID>` |
| `Model not found` | Train model: `python src/train.py` |
| `Docker daemon not running` | Start Docker: `sudo systemctl start docker` |
| `Permission denied` | Make executable: `chmod +x script.sh` |
| `Tests fail` | Ensure model trained: `python src/train.py` |

---

## 📚 Keyboard Shortcuts (Uvicorn)

- `Ctrl+C` - Stop server
- Server auto-reloads on code changes with `--reload`

---

## 🎓 Learning Resources

- **MLflow**: https://mlflow.org/docs/latest/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker**: https://docs.docker.com/
- **Pytest**: https://docs.pytest.org/

---

**Print this and keep it handy during the workshop! 📋**
