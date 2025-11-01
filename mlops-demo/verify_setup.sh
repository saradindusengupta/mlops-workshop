#!/bin/bash

# Verification Script for MLOps Demo
# This script checks that all components are properly set up

set +e  # Don't exit on error, we want to show all issues

echo "================================================"
echo "  MLOps Demo - Setup Verification"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHECKS_PASSED=0
CHECKS_FAILED=0

# Helper function
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "Running verification checks..."
echo ""

# Check 1: Python version
echo "1. Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 9 ]; then
        check_pass "Python $PYTHON_VERSION (>=3.9 required)"
    else
        check_fail "Python $PYTHON_VERSION (3.9+ required)"
    fi
else
    check_fail "Python 3 not found"
fi

# Check 2: Virtual environment
echo "2. Checking virtual environment..."
if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
    
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        check_pass "Virtual environment is activated"
    else
        check_warn "Virtual environment not activated (run: source venv/bin/activate)"
    fi
else
    check_fail "Virtual environment not found (run: python -m venv venv)"
fi

# Check 3: Dependencies
echo "3. Checking dependencies..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    PACKAGES=("pandas" "scikit-learn" "mlflow" "fastapi" "uvicorn" "pytest")
    ALL_INSTALLED=true
    
    for package in "${PACKAGES[@]}"; do
        if pip show "$package" &> /dev/null; then
            check_pass "$package installed"
        else
            check_fail "$package not installed"
            ALL_INSTALLED=false
        fi
    done
else
    check_warn "Skipping dependency check (activate venv first)"
fi

# Check 4: Data
echo "4. Checking data files..."
if [ -f "data/raw/iris.csv" ]; then
    LINES=$(wc -l < data/raw/iris.csv)
    if [ "$LINES" -eq 151 ]; then  # 150 data + 1 header
        check_pass "iris.csv exists with 150 samples"
    else
        check_warn "iris.csv exists but has $LINES lines (expected 151)"
    fi
else
    check_fail "data/raw/iris.csv not found"
fi

# Check 5: Source files
echo "5. Checking source files..."
SOURCE_FILES=("src/train.py" "src/app.py" "src/infer_schema.py" "src/__init__.py")
for file in "${SOURCE_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file not found"
    fi
done

# Check 6: Test files
echo "6. Checking test files..."
if [ -f "tests/test_infer_contract.py" ]; then
    check_pass "test_infer_contract.py exists"
else
    check_fail "tests/test_infer_contract.py not found"
fi

# Check 7: Model training
echo "7. Checking MLflow artifacts..."
if [ -d "mlruns" ]; then
    check_pass "mlruns directory exists"
    
    # Count experiments
    EXPERIMENT_COUNT=$(find mlruns -name "meta.yaml" -path "*/meta.yaml" | wc -l)
    if [ "$EXPERIMENT_COUNT" -gt 0 ]; then
        check_pass "MLflow experiments found ($EXPERIMENT_COUNT)"
    else
        check_warn "No MLflow experiments found (run: python src/train.py)"
    fi
else
    check_warn "mlruns not found (model not trained yet - run: python src/train.py)"
fi

# Check 8: Docker
echo "8. Checking Docker..."
if command -v docker &> /dev/null; then
    check_pass "Docker is installed"
    
    if docker info &> /dev/null; then
        check_pass "Docker daemon is running"
        
        # Check if image exists
        if docker images | grep -q "mlops-demo"; then
            check_pass "mlops-demo Docker image built"
        else
            check_warn "Docker image not built yet (run: docker build -t mlops-demo .)"
        fi
    else
        check_fail "Docker daemon not running"
    fi
else
    check_warn "Docker not installed (optional for workshop)"
fi

# Check 9: Configuration files
echo "9. Checking configuration files..."
CONFIG_FILES=("requirements.txt" ".gitignore" "Dockerfile" "README.md")
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file not found"
    fi
done

# Check 10: CI/CD
echo "10. Checking CI/CD configuration..."
if [ -f ".github/workflows/ci.yml" ]; then
    check_pass "GitHub Actions workflow exists"
else
    check_fail ".github/workflows/ci.yml not found"
fi

# Summary
echo ""
echo "================================================"
echo "  Verification Summary"
echo "================================================"
echo -e "${GREEN}Checks passed: $CHECKS_PASSED${NC}"
echo -e "${RED}Checks failed: $CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "You're ready to start the workshop! 🚀"
    echo ""
    echo "Next steps:"
    echo "  1. Train the model: python src/train.py"
    echo "  2. View experiments: mlflow ui"
    echo "  3. Start API: uvicorn src.app:app --reload"
    echo "  4. Run tests: pytest tests/ -v"
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Please fix the issues above before continuing."
fi

echo "================================================"
