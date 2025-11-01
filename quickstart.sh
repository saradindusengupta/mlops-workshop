#!/bin/bash

# Quick Start Script for MLOps Demo
# This script sets up the environment and runs through the demo

set -e  # Exit on error

echo "================================================"
echo "  MLOps Demo - Quick Start"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo -e "${BLUE}📦 Step 1: Setting up virtual environment${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo -e "${BLUE}📥 Step 2: Installing dependencies${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo ""
echo -e "${BLUE}🧪 Step 3: Training model with MLflow${NC}"
python mlops-demo/src/train.py
echo -e "${GREEN}✅ Model trained successfully${NC}"

echo ""
echo -e "${BLUE}🧪 Step 4: Running tests${NC}"
pytest mlops-demo/tests/ -v
echo -e "${GREEN}✅ Tests passed${NC}"

echo ""
echo "================================================"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. View MLflow experiments:"
echo "   $ mlflow ui"
echo "   Then open: http://localhost:5000"
echo ""
echo "2. Start the inference service:"
echo "   $ uvicorn mlops-demo.src.app:app --reload --port 8000"
echo "   Then open: http://localhost:8000/docs"
echo ""
echo "3. Make a prediction:"
echo '   $ curl -X POST http://localhost:8000/predict \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}'"'"
echo ""
echo "4. Build Docker image:"
echo "   $ docker build -t mlops-demo ."
echo ""
echo "5. Run containerized service:"
echo "   $ docker run -p 8000:8000 mlops-demo"
echo ""
echo "================================================"
