# MLOps Demo: From Dataset to Deployed Model

A complete, **local-first** MLOps workflow demonstrating:

- ✅ Reproducible environment and project structure
- ✅ Data versioning (optional with DVC)
- ✅ Experiment tracking with MLflow
- ✅ Model registration
- ✅ FastAPI inference service with contract validation
- ✅ Containerization with Docker
- ✅ CI/CD with GitHub Actions

Perfect for learning MLOps fundamentals without cloud dependencies!

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerization)
- Git

### Setup

1. **Clone and navigate**

```bash
cd mlops-demo
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
mlops-demo/
├── data/
│   └── raw/
│       └── iris.csv          # Training dataset
├── src/
│   ├── train.py              # Training script with MLflow tracking
│   ├── app.py                # FastAPI inference service
│   └── infer_schema.py       # Inference contract definition
├── tests/
│   └── test_infer_contract.py # API smoke tests
├── .github/
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
├── .gitignore             
└── README.md
```

---

## 🎯 Step-by-Step Walkthrough

### Step 1: Data Setup (Optional: DVC)

The Iris dataset is already included in `data/raw/iris.csv`.

**Optional DVC setup** for data versioning:

```bash
pip install dvc
dvc init
dvc add data/raw/iris.csv
git add data/raw/iris.csv.dvc data/.gitignore
git commit -m "Track data with DVC"
```

---

### Step 2: Train Model with MLflow

Train a simple Random Forest classifier with experiment tracking:

```bash
python src/train.py
```

**What happens:**

- Loads Iris dataset
- Trains a Random Forest model
- Logs parameters, metrics, and the model to MLflow
- Registers the model in MLflow Model Registry

**View experiments:**

```bash
mlflow ui
```

Visit `http://localhost:5000` to explore logged experiments.

---

### Step 3: Inference Service with FastAPI

Start the inference API:

```bash
uvicorn src.app:app --reload --port 8000
```

**Test the API:**

```bash
# Health check
curl http://localhost:8000/health

# Get inference contract
curl http://localhost:8000/contract

# Make a prediction
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

**Interactive docs:** Visit `http://localhost:8000/docs`

---

### Step 4: Run Tests

Execute smoke tests to validate the API contract:

```bash
pytest tests/ -v
```

---

### Step 5: Dockerize the Service

Build the Docker image:

```bash
docker build -t mlops-demo:latest .
```

Run the containerized service:

```bash
docker run -p 8000:8000 mlops-demo:latest
```

Test the containerized API:

```bash
curl http://localhost:8000/health
```

---

### Step 6: CI/CD Pipeline

The `.github/workflows/ci.yml` file defines an automated pipeline that:

- Installs dependencies
- Runs tests
- Builds Docker image
- (Optional) Pushes to registry

**Trigger it:** Push to GitHub and watch the Actions tab.

---

## 🧪 API Contract

The inference service follows a strict contract defined in `infer_schema.py`:

**Input:**

```json
{
  "features": {
    "sepal_length": float,
    "sepal_width": float,
    "petal_length": float,
    "petal_width": float
  }
}
```

**Output:**

```json
{
  "prediction": int,
  "prediction_label": str,
  "confidence": float,
  "model_version": str
}
```

---

## 📊 MLflow Tracking

Every training run logs:

- **Parameters:** `n_estimators`, `max_depth`, `random_state`
- **Metrics:** `accuracy`, `f1_score`
- **Artifacts:** Trained model (`.pkl`)
- **Tags:** `dataset`, `framework`

Models are registered in the MLflow Model Registry for versioning and stage management.

---

## 🛠 Development Workflow

1. **Experiment:** Modify hyperparameters in `train.py`
2. **Track:** View results in MLflow UI
3. **Deploy:** Update model path in `app.py`
4. **Test:** Run `pytest tests/`
5. **Containerize:** Rebuild Docker image
6. **CI/CD:** Push to trigger automated checks

---

## 🎓 Learning Outcomes

By completing this demo, you'll understand:

- Reproducible ML project structure
- Experiment tracking and model registry
- API-first model deployment
- Contract-driven inference design
- Containerization best practices
- Automated testing and CI/CD

---

## 🔧 Troubleshooting

**Issue: MLflow UI not starting**

- Ensure port 5000 is free
- Check `mlruns/` directory exists

**Issue: Docker build fails**

- Verify Docker is running
- Check Dockerfile syntax

**Issue: Tests fail**

- Ensure model exists in `mlruns/`
- Check FastAPI service is running

---

## 📚 Next Steps

- Add model monitoring and drift detection
- Implement A/B testing
- Set up model versioning strategy
- Add performance benchmarking
- Integrate with cloud services (AWS, Azure, GCP)

---

## 🤝 Contributing

This is a learning project! Feel free to:

- Add new features
- Improve documentation
- Share feedback

---

## 📄 License

MIT License - Free to use for education and commercial purposes.

---

**Built with ❤️ for MLOps learners**
