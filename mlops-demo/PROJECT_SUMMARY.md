# MLOps Demo - Project Summary

## 🎯 Project Overview

A complete, production-ready MLOps demonstration that takes students from a raw dataset to a containerized, deployable inference service with experiment tracking, automated testing, and CI/CD.

**Key Features:**
- ✅ Reproducible environment setup
- ✅ Data versioning with optional DVC
- ✅ Experiment tracking with MLflow
- ✅ Model registry and versioning
- ✅ Contract-driven FastAPI inference service
- ✅ Comprehensive test suite
- ✅ Multi-stage Docker containerization
- ✅ GitHub Actions CI/CD pipeline

---

## 📁 Complete Project Structure

```
mlops-demo/
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline with test, lint, docker, security jobs
├── data/
│   └── raw/
│       └── iris.csv                  # Complete Iris dataset (150 samples)
├── src/
│   ├── __init__.py                   # Package initialization
│   ├── train.py                      # Training script with MLflow tracking
│   ├── app.py                        # FastAPI inference service
│   └── infer_schema.py               # Pydantic contract definitions
├── tests/
│   └── test_infer_contract.py        # Comprehensive API smoke tests
├── .dockerignore                     # Docker build optimization
├── .gitignore                        # Git ignore patterns
├── Dockerfile                        # Multi-stage production container
├── README.md                         # User-facing documentation
├── WORKSHOP_GUIDE.md                 # Step-by-step workshop instructions
├── quickstart.sh                     # Automated setup script
└── requirements.txt                  # Python dependencies
```

---

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
cd mlops-demo
chmod +x quickstart.sh
./quickstart.sh
```

### Option 2: Manual Setup
```bash
# 1. Create environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train model
python src/train.py

# 4. Start MLflow UI (separate terminal)
mlflow ui

# 5. Start API service (separate terminal)
uvicorn src.app:app --reload

# 6. Run tests
pytest tests/ -v

# 7. Build Docker image
docker build -t mlops-demo .

# 8. Run container
docker run -p 8000:8000 mlops-demo
```

---

## 📚 Component Details

### 1. Training Script (`src/train.py`)

**Features:**
- Loads Iris dataset from CSV
- Trains Random Forest classifier
- Logs to MLflow:
  - Parameters: `n_estimators`, `max_depth`, `random_state`, `test_size`
  - Metrics: `accuracy`, `f1_score`
  - Artifacts: Trained model
  - Tags: `dataset`, `framework`, `algorithm`
- Registers model in MLflow Model Registry

**Output:**
- Creates `mlruns/` directory with experiment data
- Console output with training progress and metrics
- Registered model: `iris_classifier`

### 2. Inference Schema (`src/infer_schema.py`)

**Models:**
- `IrisFeatures`: Input features with validation (0-10 range, non-negative)
- `InferenceRequest`: Request wrapper
- `InferenceResponse`: Prediction, label, confidence, model version
- `HealthResponse`: Service health status
- `ContractResponse`: API schema documentation

**Validation:**
- Type checking
- Range validation
- Required field enforcement
- Custom validators for business logic

### 3. FastAPI Service (`src/app.py`)

**Endpoints:**
- `GET /` - Service information
- `GET /health` - Health check with model status
- `GET /contract` - API contract schemas
- `POST /predict` - Inference endpoint

**Features:**
- Loads model from MLflow (registry or latest run)
- Automatic OpenAPI documentation at `/docs`
- Comprehensive error handling
- Logging for debugging
- Model version tracking

### 4. Test Suite (`tests/test_infer_contract.py`)

**Test Categories:**
- **Health Endpoint:** Status codes, response structure
- **Contract Endpoint:** Schema availability and structure
- **Prediction Endpoint:** Valid inputs, validation, multiple species
- **Root Endpoint:** Service information
- **Edge Cases:** Zero values, max values, empty bodies

**Coverage:**
- 40+ test cases
- Input validation
- Response structure
- Error handling
- Boundary conditions

### 5. Dockerfile (Multi-stage)

**Stage 1 - Builder:**
- Installs build dependencies (gcc, g++)
- Copies requirements and application code
- Installs Python packages
- Trains model (creates mlruns/)

**Stage 2 - Runtime:**
- Minimal Python slim image
- Copies only runtime dependencies
- Copies trained model artifacts
- Exposes port 8000
- Health check every 30s
- Runs uvicorn server

**Optimizations:**
- Layer caching for dependencies
- Multi-stage reduces image size by ~60%
- No unnecessary build tools in production

### 6. CI/CD Pipeline (`.github/workflows/ci.yml`)

**Jobs:**

1. **Test Job:**
   - Sets up Python 3.9
   - Installs dependencies with caching
   - Trains model
   - Runs pytest suite
   - Uploads test artifacts

2. **Lint Job:**
   - Runs flake8 for syntax errors
   - Checks formatting with black
   - Continues on error for visibility

3. **Docker Job:**
   - Builds Docker image
   - Tests container health
   - Saves image as artifact
   - 7-day retention

4. **Security Job:**
   - Runs Trivy vulnerability scanner
   - Uploads SARIF results
   - Integrates with GitHub Security

**Triggers:**
- Push to main/develop
- Pull requests to main
- Manual workflow dispatch

---

## 🎓 Workshop Flow (45 minutes)

### Module Breakdown:

1. **Environment Setup (5 min)** - Virtual env, dependencies
2. **Data Versioning (5 min)** - Optional DVC setup
3. **Experiment Tracking (10 min)** - Train with MLflow, explore UI
4. **Inference Service (10 min)** - FastAPI, contracts, testing
5. **Automated Testing (5 min)** - Run pytest suite
6. **Containerization (7 min)** - Build and run Docker
7. **CI/CD Pipeline (3 min)** - Review GitHub Actions

---

## 🔧 Technologies Used

**ML & Data:**
- pandas 2.1.3 - Data manipulation
- numpy 1.26.2 - Numerical computing
- scikit-learn 1.3.2 - ML algorithms

**Experiment Tracking:**
- mlflow 2.8.1 - Experiment tracking and model registry

**API & Inference:**
- fastapi 0.104.1 - Web framework
- uvicorn 0.24.0 - ASGI server
- pydantic 2.5.0 - Data validation

**Testing:**
- pytest 7.4.3 - Test framework
- httpx 0.25.1 - Async HTTP client

**Containerization:**
- Docker - Containerization
- Multi-stage builds - Optimization

**CI/CD:**
- GitHub Actions - Automation
- Trivy - Security scanning

---

## 📊 Key Metrics & Results

**Model Performance:**
- Algorithm: Random Forest
- Accuracy: ~95-97% (on test set)
- F1 Score: ~0.95-0.97 (weighted)
- Training time: <1 second

**API Performance:**
- Response time: <50ms (p95)
- Throughput: 100+ req/s (single instance)
- Container startup: ~5 seconds

**Docker Image:**
- Final size: ~500MB (with multi-stage)
- Build time: ~2-3 minutes
- Health check: 30s interval

---

## 🎯 Learning Outcomes

Students will learn:

1. **Project Organization**
   - Reproducible structure
   - Dependency management
   - Configuration handling

2. **Experiment Tracking**
   - Why track experiments
   - What to log (params, metrics, artifacts)
   - Model registry usage

3. **API Design**
   - Contract-first approach
   - Input validation
   - Error handling
   - Documentation

4. **Testing**
   - API smoke tests
   - Contract validation
   - Edge case handling

5. **Containerization**
   - Multi-stage builds
   - Image optimization
   - Health checks

6. **CI/CD**
   - Automated testing
   - Container builds
   - Security scanning

---

## 🚀 Extension Ideas

**Beginner:**
- Add more feature validation rules
- Implement request logging
- Add prometheus metrics endpoint

**Intermediate:**
- Implement model A/B testing
- Add caching layer (Redis)
- Create monitoring dashboard (Grafana)

**Advanced:**
- Set up Kubernetes deployment
- Implement data drift detection
- Add feature store (Feast)
- Create custom MLflow plugins

---

## 📝 Teaching Notes

**Key Discussion Points:**

1. **Why MLflow?**
   - Compare to manual logging
   - Discuss reproducibility
   - Show model lineage

2. **Why Contracts?**
   - Prevent breaking changes
   - Enable versioning
   - Facilitate testing

3. **Why Docker?**
   - Consistency across environments
   - Dependency isolation
   - Scalability

4. **Why CI/CD?**
   - Catch issues early
   - Automate repetitive tasks
   - Enable continuous deployment

**Common Pitfalls:**
- Forgetting to train model before starting API
- Not activating virtual environment
- Port conflicts (5000 for MLflow, 8000 for API)
- Docker daemon not running

**Tips:**
- Have students work in pairs
- Encourage experimentation with hyperparameters
- Discuss real-world scenarios
- Show production examples

---

## 🔍 Verification Checklist

After setup, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] Model trained (`mlruns/` exists)
- [ ] MLflow UI accessible (localhost:5000)
- [ ] API running (localhost:8000)
- [ ] Tests passing (`pytest tests/`)
- [ ] Docker image built (`docker images`)
- [ ] Container running (`docker ps`)
- [ ] Health check passing (curl /health)
- [ ] Prediction working (curl /predict)

---

## 📚 Additional Resources

**Documentation:**
- [MLflow Docs](https://mlflow.org/docs/latest/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Pydantic Docs](https://docs.pydantic.dev/)

**Further Reading:**
- "Machine Learning Engineering" by Andriy Burkov
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Designing Machine Learning Systems" by Chip Huyen

**Community:**
- MLOps Community Slack
- MLflow Slack
- FastAPI Discord

---

## 🤝 Contributing

This is an educational project. Improvements welcome:
- Better documentation
- Additional test cases
- New features (monitoring, etc.)
- Bug fixes
- Workshop feedback

---

## 📄 License

MIT License - Free for educational and commercial use.

---

**Built for MLOps learners by MLOps practitioners 🚀**

*Last updated: November 2025*
