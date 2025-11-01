"""
Smoke tests for the Iris Classification API.

Tests the basic functionality of the inference service including:
- Health check
- Contract endpoint
- Prediction endpoint
- Input validation
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_status_code(self):
        """Test that health endpoint returns 200 or 503."""
        response = client.get("/health")
        assert response.status_code in [200, 503], "Health check should return 200 or 503"
    
    def test_health_check_structure(self):
        """Test that health response has required fields."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data, "Health response should include 'status'"
        assert "model_loaded" in data, "Health response should include 'model_loaded'"
        assert data["status"] in ["healthy", "unhealthy"], "Status must be 'healthy' or 'unhealthy'"


class TestContractEndpoint:
    """Tests for the contract endpoint."""
    
    def test_contract_returns_200(self):
        """Test that contract endpoint returns 200."""
        response = client.get("/contract")
        assert response.status_code == 200, "Contract endpoint should return 200"
    
    def test_contract_has_schemas(self):
        """Test that contract includes input and output schemas."""
        response = client.get("/contract")
        data = response.json()
        
        assert "input_schema" in data, "Contract should include 'input_schema'"
        assert "output_schema" in data, "Contract should include 'output_schema'"
    
    def test_contract_input_schema_structure(self):
        """Test that input schema has expected structure."""
        response = client.get("/contract")
        data = response.json()
        input_schema = data["input_schema"]
        
        # Check for properties in nested structure
        assert "properties" in input_schema or "$defs" in input_schema, \
            "Input schema should have properties or definitions"
    
    def test_contract_output_schema_structure(self):
        """Test that output schema has expected structure."""
        response = client.get("/contract")
        data = response.json()
        output_schema = data["output_schema"]
        
        # Check for properties in nested structure
        assert "properties" in output_schema or "$defs" in output_schema, \
            "Output schema should have properties or definitions"


class TestPredictionEndpoint:
    """Tests for the prediction endpoint."""
    
    @pytest.fixture
    def valid_request(self):
        """Valid request payload for prediction."""
        return {
            "features": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }
    
    def test_predict_with_valid_input(self, valid_request):
        """Test prediction with valid input."""
        response = client.post("/predict", json=valid_request)
        
        # Should return 200 if model is loaded, 503 if not
        assert response.status_code in [200, 503], \
            "Predict should return 200 (success) or 503 (model not loaded)"
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            assert "prediction" in data, "Response should include 'prediction'"
            assert "prediction_label" in data, "Response should include 'prediction_label'"
            assert "confidence" in data, "Response should include 'confidence'"
            assert "model_version" in data, "Response should include 'model_version'"
            
            # Check data types
            assert isinstance(data["prediction"], int), "Prediction should be an integer"
            assert isinstance(data["prediction_label"], str), "Prediction label should be a string"
            assert isinstance(data["confidence"], float), "Confidence should be a float"
            
            # Check value ranges
            assert 0 <= data["prediction"] <= 2, "Prediction should be 0, 1, or 2"
            assert 0 <= data["confidence"] <= 1, "Confidence should be between 0 and 1"
            assert data["prediction_label"] in ["setosa", "versicolor", "virginica"], \
                "Label should be a valid species"
    
    def test_predict_validates_required_fields(self):
        """Test that missing required fields are rejected."""
        invalid_request = {
            "features": {
                "sepal_length": 5.1,
                # Missing other required fields
            }
        }
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422, "Should return 422 for missing fields"
    
    def test_predict_validates_data_types(self):
        """Test that invalid data types are rejected."""
        invalid_request = {
            "features": {
                "sepal_length": "not_a_number",  # Invalid type
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422, "Should return 422 for invalid data types"
    
    def test_predict_validates_negative_values(self):
        """Test that negative values are rejected."""
        invalid_request = {
            "features": {
                "sepal_length": -1.0,  # Negative value
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422, "Should return 422 for negative values"
    
    def test_predict_multiple_species(self):
        """Test predictions for different species."""
        test_cases = [
            # Setosa (should predict 0)
            {
                "features": {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                }
            },
            # Versicolor (should predict 1)
            {
                "features": {
                    "sepal_length": 6.0,
                    "sepal_width": 2.7,
                    "petal_length": 5.1,
                    "petal_width": 1.6
                }
            },
            # Virginica (should predict 2)
            {
                "features": {
                    "sepal_length": 7.2,
                    "sepal_width": 3.0,
                    "petal_length": 5.8,
                    "petal_width": 1.6
                }
            }
        ]
        
        for test_case in test_cases:
            response = client.post("/predict", json=test_case)
            
            # Only check if model is loaded
            if response.status_code == 200:
                data = response.json()
                assert "prediction" in data
                assert 0 <= data["prediction"] <= 2


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200."""
        response = client.get("/")
        assert response.status_code == 200, "Root endpoint should return 200"
    
    def test_root_has_service_info(self):
        """Test that root endpoint includes service information."""
        response = client.get("/")
        data = response.json()
        
        assert "service" in data, "Root should include 'service'"
        assert "version" in data, "Root should include 'version'"
        assert "endpoints" in data, "Root should include 'endpoints'"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_predict_with_zero_values(self):
        """Test prediction with all zeros."""
        request = {
            "features": {
                "sepal_length": 0.0,
                "sepal_width": 0.0,
                "petal_length": 0.0,
                "petal_width": 0.0
            }
        }
        
        response = client.post("/predict", json=request)
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 422, 500, 503]
    
    def test_predict_with_max_values(self):
        """Test prediction with maximum allowed values."""
        request = {
            "features": {
                "sepal_length": 10.0,
                "sepal_width": 10.0,
                "petal_length": 10.0,
                "petal_width": 10.0
            }
        }
        
        response = client.post("/predict", json=request)
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 422, 500, 503]
    
    def test_predict_with_empty_body(self):
        """Test prediction with empty request body."""
        response = client.post("/predict", json={})
        assert response.status_code == 422, "Should return 422 for empty body"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
