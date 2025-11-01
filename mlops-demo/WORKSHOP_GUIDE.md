# MLOps Workshop Guide

## Workshop Overview

**Duration:** ~45 minutes  
**Level:** Beginner to Intermediate  
**Prerequisites:** Basic Python, Docker, and Git knowledge

### Learning Objectives

By the end of this workshop, you will:
- Understand end-to-end MLOps workflow
- Implement experiment tracking with MLflow
- Build contract-driven inference APIs
- Containerize ML services
- Set up CI/CD for ML applications

---

## Workshop Structure

### Step 1: Repository Structure and Environment Setup (5 min)

**What you'll learn:**
- Organizing ML projects for reproducibility
- Setting up isolated Python environments
- Managing dependencies

**Instructions:**

1. Navigate to the project:
```bash
cd mlops-demo
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Key Concepts:**
- **Virtual environments** isolate project dependencies
- **requirements.txt** ensures reproducible installations
- **Proper structure** makes projects maintainable

**Discussion Points:**
- Why is reproducibility important in ML?
- What problems does dependency isolation solve?
- How would you handle different dependency versions across projects?

---

### Step 2: Data Versioning with DVC (Optional, 5 min)

**What you'll learn:**
- Version control for datasets
- Tracking data lineage
- Collaborative data management

**Instructions:**

1. Initialize DVC:
```bash
pip install dvc
dvc init
```

2. Track the dataset:
```bash
dvc add data/raw/iris.csv
git add data/raw/iris.csv.dvc data/.gitignore
git commit -m "Track iris dataset with DVC"
```

**Key Concepts:**
- **DVC** versions large files efficiently
- **.dvc files** store metadata, not actual data
- **Remote storage** enables team collaboration

**Discussion Points:**
- When should you version your data?
- What are the trade-offs of data versioning?
- How does DVC compare to storing data in Git LFS or cloud storage?

---

### Step 3: Experiment Tracking with MLflow (10 min)

**What you'll learn:**
- Logging experiments systematically
- Comparing model performance
- Managing model artifacts

**Instructions:**

1. Review the training script:
```bash
cat src/train.py
```

Key components:
- Data loading and preprocessing
- Model training with hyperparameters
- MLflow logging (params, metrics, model)
- Model registration

2. Run the training script:
```bash
python src/train.py
```

3. Start MLflow UI:
```bash
mlflow ui
```

4. Open browser to `http://localhost:5000`

5. Explore:
   - Runs table with metrics
   - Run details with parameters
   - Model artifacts
   - Model registry

**Key Concepts:**
- **Experiment tracking** records all training runs
- **Parameters** are model hyperparameters
- **Metrics** measure model performance
- **Artifacts** store models and outputs
- **Model registry** versions production models

**Exercise:**
Modify hyperparameters in `train.py` and rerun:
```python
# Try different values:
n_estimators = 200  # from 100
max_depth = 10      # from 5
```

Compare results in MLflow UI.

**Discussion Points:**
- What experiments would you track for a production ML system?
- How do you decide which metrics to log?
- When should you register a model to the registry?

---

### Step 4: Inference Contract and FastAPI Service (10 min)

**What you'll learn:**
- Designing API contracts
- Building REST APIs for ML
- Input validation and error handling

**Instructions:**

1. Review the contract definition:
```bash
cat src/infer_schema.py
```

Key components:
- `InferenceRequest` - input schema with validation
- `InferenceResponse` - output schema with guarantees
- `HealthResponse` and `ContractResponse` for monitoring

2. Review the FastAPI service:
```bash
cat src/app.py
```

Key components:
- Model loading from MLflow
- `/health` endpoint for monitoring
- `/contract` endpoint for discoverability
- `/predict` endpoint for inference

3. Start the service:
```bash
uvicorn src.app:app --reload --port 8000
```

4. Open interactive docs: `http://localhost:8000/docs`

5. Test endpoints:

**Health check:**
```bash
curl http://localhost:8000/health
```

**Get contract:**
```bash
curl http://localhost:8000/contract
```

**Make prediction:**
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

**Key Concepts:**
- **Contract-first design** defines clear expectations
- **Pydantic validation** ensures data quality
- **FastAPI** auto-generates OpenAPI docs
- **Type safety** catches errors early

**Exercise:**
Try invalid inputs:
```bash
# Negative values
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": -1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}'

# Missing fields
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": 5.1}}'
```

**Discussion Points:**
- Why is contract validation important for ML APIs?
- What should you include in error responses?
- How do you handle model versioning in production?

---

### Step 5: Automated Testing (5 min)

**What you'll learn:**
- Testing ML APIs
- Smoke tests vs integration tests
- Test-driven development for ML

**Instructions:**

1. Review test structure:
```bash
cat tests/test_infer_contract.py
```

Test categories:
- Health endpoint tests
- Contract endpoint tests
- Prediction endpoint tests
- Input validation tests
- Edge case tests

2. Run tests:
```bash
pytest tests/ -v
```

3. Run with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

**Key Concepts:**
- **Smoke tests** verify basic functionality
- **Contract tests** ensure API compatibility
- **Edge case tests** catch boundary conditions
- **Test automation** catches regressions

**Exercise:**
Add a new test for a different iris species:
```python
def test_predict_virginica(self):
    request = {
        "features": {
            "sepal_length": 7.0,
            "sepal_width": 3.2,
            "petal_length": 4.7,
            "petal_width": 1.4
        }
    }
    response = client.post("/predict", json=request)
    assert response.status_code == 200
```

**Discussion Points:**
- What types of tests are critical for ML systems?
- How do you test model quality vs API functionality?
- Should you mock the model in API tests?

---

### Step 6: Containerization with Docker (7 min)

**What you'll learn:**
- Multi-stage Docker builds
- Optimizing image size
- Container best practices

**Instructions:**

1. Review Dockerfile:
```bash
cat Dockerfile
```

Key features:
- **Multi-stage build** separates build and runtime
- **Builder stage** trains model and installs deps
- **Runtime stage** creates minimal production image
- **Health check** enables container monitoring

2. Build the image:
```bash
docker build -t mlops-demo:latest .
```

3. Run the container:
```bash
docker run -p 8000:8000 mlops-demo:latest
```

4. Test the containerized service:
```bash
curl http://localhost:8000/health
```

5. Check container health:
```bash
docker ps
# Look for health status
```

**Key Concepts:**
- **Multi-stage builds** reduce image size
- **Layer caching** speeds up builds
- **Health checks** enable orchestration
- **Immutable artifacts** ensure reproducibility

**Exercise:**
Compare image sizes:
```bash
docker images | grep mlops-demo
```

**Discussion Points:**
- What are the benefits of containerization for ML?
- When should you train models during build vs runtime?
- How do you handle large models in containers?

---

### Step 7: CI/CD Pipeline (5 min)

**What you'll learn:**
- Automating ML workflows
- Continuous testing
- Deployment automation

**Instructions:**

1. Review the CI/CD workflow:
```bash
cat .github/workflows/ci.yml
```

Pipeline stages:
- **Test job:** Installs deps, trains model, runs tests
- **Lint job:** Checks code quality
- **Docker job:** Builds and tests container
- **Security job:** Scans for vulnerabilities

2. Pipeline triggers:
   - Push to main/develop branches
   - Pull requests
   - Manual workflow dispatch

3. Artifacts:
   - Test results
   - Docker images
   - Security reports

**Key Concepts:**
- **Automated testing** catches issues early
- **Container builds** ensure deployability
- **Security scanning** identifies vulnerabilities
- **Artifact storage** preserves build outputs

**Discussion Points:**
- What should trigger model retraining in production?
- How do you handle model validation in CI/CD?
- What's the difference between CI and CD for ML?

---

## Complete Workflow Demo

Run the entire workflow end-to-end:

```bash
# 1. Train model
python src/train.py

# 2. Start MLflow UI (in separate terminal)
mlflow ui

# 3. Start API service (in separate terminal)
uvicorn src.app:app --reload

# 4. Run tests
pytest tests/ -v

# 5. Build Docker image
docker build -t mlops-demo .

# 6. Run containerized service
docker run -p 8000:8000 mlops-demo
```

---

## Advanced Topics (If Time Permits)

### Model Monitoring
- Tracking prediction distributions
- Detecting data drift
- Performance degradation alerts

### A/B Testing
- Canary deployments
- Feature flags
- Experiment analysis

### Scaling
- Kubernetes deployment
- Load balancing
- Auto-scaling policies

---

## Common Troubleshooting

### Issue: MLflow can't find runs
**Solution:** Check MLflow tracking URI
```bash
export MLFLOW_TRACKING_URI=mlruns
```

### Issue: FastAPI can't load model
**Solution:** Train model first
```bash
python src/train.py
```

### Issue: Docker build fails
**Solution:** Check Docker daemon
```bash
docker info
```

### Issue: Tests fail
**Solution:** Ensure model is trained
```bash
python src/train.py
pytest tests/ -v
```

---

## Next Steps

After the workshop, explore:

1. **Model Versioning:** Implement A/B testing with multiple models
2. **Monitoring:** Add Prometheus metrics and Grafana dashboards
3. **Feature Store:** Centralize feature engineering
4. **Drift Detection:** Monitor input and output distributions
5. **Cloud Deployment:** Deploy to AWS, Azure, or GCP
6. **Kubernetes:** Orchestrate with Helm charts
7. **Feature Flags:** Decouple deployment from release

---

## Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Pydantic](https://docs.pydantic.dev/)

---

## Feedback

Share your experience:
- What worked well?
- What was confusing?
- What would you like to learn more about?

---

**Happy Learning! 🚀**
