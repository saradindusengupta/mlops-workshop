# Instructor Guide - MLOps Workshop

## 📋 Pre-Workshop Checklist

### Before the Workshop Day

- [ ] Test complete workflow on your machine
- [ ] Ensure Docker is installed and working
- [ ] Verify all scripts execute successfully
- [ ] Prepare backup USB drives with dependencies
- [ ] Test internet connectivity at venue
- [ ] Have offline documentation ready

### Materials Needed

- Workshop laptop/projector setup
- Student handouts (print CHEATSHEET.md)
- USB drives with pre-downloaded dependencies
- Sample `.whl` files for offline installation
- Backup slides (if needed)

---

## 🎯 Workshop Execution Plan

### Pre-Session (15 min before start)

1. **Room Setup**
   - Test projector/screen
   - Verify internet connection
   - Open terminal windows ready
   - Have MLflow UI pre-loaded
   - Open API docs in browser

2. **Student Arrival**
   - Share GitHub repository link
   - Distribute cheat sheets
   - Quick environment checks
   - Offer help with setup issues

---

## 📚 Session Breakdown (45 minutes)

### Opening (3 min)
- Introduce yourself and workshop goals
- Set expectations (hands-on, ask questions)
- Quick poll: Who has used MLflow? Docker? FastAPI?

### Part 1: Setup & Data (5 min)

**Instructor Actions:**
```bash
cd mlops-demo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./verify_setup.sh
```

**Teaching Points:**
- Why virtual environments matter
- Importance of reproducible setups
- Quick tour of project structure

**Common Issues:**
- Python version mismatches → Use pyenv
- Slow pip install → Pre-downloaded wheels
- Permission errors → chmod +x scripts

### Part 2: Training with MLflow (10 min)

**Instructor Actions:**
```bash
# Terminal 1
python src/train.py

# Terminal 2  
mlflow ui
```

**Live Demo Flow:**
1. Open `src/train.py` - explain structure
2. Run training - watch console output
3. Switch to MLflow UI
4. Explore:
   - Experiments table
   - Run details
   - Parameters vs Metrics
   - Model artifacts
   - Model registry

**Teaching Points:**
- Why track experiments?
- What to log (params, metrics, artifacts)
- Model versioning strategies
- Comparing runs

**Hands-On Exercise:**
"Change `n_estimators` to 200 and retrain. Compare results in MLflow."

### Part 3: API Development (12 min)

**Instructor Actions:**
```bash
# Show files first
cat src/infer_schema.py  # Explain contracts
cat src/app.py           # Explain FastAPI

# Start service
uvicorn src.app:app --reload
```

**Live Demo Flow:**
1. Open API docs at localhost:8000/docs
2. Test each endpoint interactively:
   - GET /health
   - GET /contract
   - POST /predict (use examples)
3. Show curl commands in terminal
4. Demonstrate validation errors

**Teaching Points:**
- Contract-first API design
- Why validate inputs?
- FastAPI auto-documentation
- Error handling strategies

**Hands-On Exercise:**
"Make 3 predictions with different iris species using curl or the docs."

### Part 4: Testing (5 min)

**Instructor Actions:**
```bash
pytest tests/ -v
pytest tests/ -v --cov=src --cov-report=term
```

**Teaching Points:**
- Why test ML APIs?
- Types of tests (smoke, integration, contract)
- Coverage as a metric
- Testing vs monitoring

**Quick Demo:**
- Show test file structure
- Run tests with verbose output
- Show coverage report

### Part 5: Containerization (7 min)

**Instructor Actions:**
```bash
# Show Dockerfile
cat Dockerfile  # Explain multi-stage

# Build (may take 2-3 min)
docker build -t mlops-demo .

# Run
docker run -d -p 8000:8000 --name mlops-demo mlops-demo

# Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}'
```

**Teaching Points:**
- Why containerize?
- Multi-stage builds (show size difference)
- Health checks in production
- Environment variables

**If Time Permits:**
```bash
docker exec -it mlops-demo /bin/bash
# Show inside container
ls -la
exit
```

### Part 6: CI/CD (3 min)

**Instructor Actions:**
```bash
cat .github/workflows/ci.yml
```

**Teaching Points:**
- Automation benefits
- CI vs CD for ML
- What to test in pipeline
- When to retrain models

**Show Diagram:**
```
Code Push → Test → Build → Deploy
    ↓         ↓       ↓        ↓
  Lint    Model  Docker   Registry
         Train    Test
```

### Closing (5 min)

**Wrap-Up:**
- Recap key concepts
- Share resources (README.md links)
- Next steps suggestions
- Q&A

**Take-Home Challenge:**
"Add a new endpoint that returns feature importance from the model."

---

## 🎤 Speaking Notes

### Key Messages to Emphasize

1. **Reproducibility First**
   - "If you can't reproduce it, you can't trust it in production"
   - Environment management is not optional

2. **Experiment Tracking**
   - "You'll run hundreds of experiments - don't trust your memory"
   - MLflow makes collaboration possible

3. **Contracts Matter**
   - "Breaking API changes break production systems"
   - Define contracts before implementing

4. **Test Everything**
   - "ML bugs are silent - they don't crash, they just give wrong answers"
   - Tests catch integration issues

5. **Containers Solve Problems**
   - "It works on my machine → It works everywhere"
   - Isolation and portability

### Pacing Tips

- **Too Fast?** Add more explanation at each step
- **Too Slow?** Skip DVC section, shorten testing demo
- **Questions?** Budget 2-3 min for Q&A after each section

---

## 🔧 Troubleshooting Guide

### Student Environment Issues

| Issue | Quick Fix |
|-------|-----------|
| Old Python | Install Python 3.9+ or use pyenv |
| No Docker | Skip containerization, show pre-built |
| Slow internet | Use USB with pre-downloaded deps |
| Port conflicts | Use different ports (8001, 5001) |
| Import errors | Verify venv activated |
| Model not found | Run train.py first |

### Live Demo Failures

**Plan B Options:**
- Pre-recorded video backup
- Pre-trained model artifacts
- Screen recordings of each section
- Pair students for collaborative debugging

### Time Management

**Running Behind:**
- Skip DVC entirely
- Shorten testing demo (just show it works)
- Pre-build Docker image

**Running Ahead:**
- Deep dive into MLflow features
- Show more complex predictions
- Discuss production considerations
- Live debugging session

---

## 📊 Assessment Opportunities

### Check Understanding

**After Training:**
- "What parameters did we log?"
- "Where is the model saved?"
- "How would you find the best run?"

**After API:**
- "What happens if you send invalid data?"
- "How do you version the API?"
- "What's in the response?"

**After Docker:**
- "Why two stages in Dockerfile?"
- "How do you update the model?"
- "What if the container crashes?"

---

## 🎓 Extension Topics (If Time)

### Advanced Concepts (5-10 min each)

1. **Model Monitoring**
   - Show how to log predictions
   - Discuss drift detection
   - Alert strategies

2. **A/B Testing**
   - Load two models
   - Random routing
   - Metric comparison

3. **Scaling**
   - Multiple uvicorn workers
   - Load balancing
   - Kubernetes basics

4. **Feature Stores**
   - Why centralize features?
   - Feast introduction
   - Training-serving skew

---

## 📝 Post-Workshop

### Follow-Up Materials

**Send to Students:**
- [ ] Link to GitHub repo
- [ ] Additional resources list
- [ ] Survey for feedback
- [ ] Certificate (if applicable)
- [ ] Slack/Discord channel invite

### Gather Feedback

Questions to ask:
- What was most valuable?
- What was confusing?
- Pacing appropriate?
- What would you add/remove?
- Would you recommend to others?

---

## 🚀 Making It Your Own

### Customization Ideas

**Different Dataset:**
- Swap iris.csv with your data
- Update schema in infer_schema.py
- Adjust train.py accordingly

**Different Model:**
- Try XGBoost, LightGBM
- Deep learning with TensorFlow/PyTorch
- Time series with Prophet

**Different API Features:**
- Batch predictions
- Streaming inference
- Model explanations (SHAP)

**Production Features:**
- Redis caching
- Prometheus metrics
- Structured logging
- Rate limiting

---

## 📚 Resource Links

### Documentation
- [MLflow Docs](https://mlflow.org/docs/latest/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Docs](https://docs.docker.com/)
- [Pytest Docs](https://docs.pytest.org/)

### Tutorials
- [MLflow Tutorial](https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Docker for Beginners](https://docker-curriculum.com/)

### Books
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Designing Machine Learning Systems" by Chip Huyen
- "Machine Learning Engineering" by Andriy Burkov

### Communities
- [MLOps Community](https://mlops.community/)
- [r/MachineLearning](https://reddit.com/r/MachineLearning)
- [r/MLOps](https://reddit.com/r/mlops)

---

## ✅ Final Checklist

Before starting:
- [ ] All scripts tested
- [ ] Docker working
- [ ] Backup plans ready
- [ ] Materials printed
- [ ] Room setup done
- [ ] Timing rehearsed

During workshop:
- [ ] Engage students
- [ ] Check understanding
- [ ] Manage time
- [ ] Handle questions
- [ ] Stay on track

After workshop:
- [ ] Gather feedback
- [ ] Send follow-ups
- [ ] Update materials
- [ ] Document issues

---

**Good luck with your workshop! 🎉**

*Remember: Students learn by doing. Make it interactive, make it fun, and don't worry about perfection.*
