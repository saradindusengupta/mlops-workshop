"""
Inference contract definition using Pydantic.

Defines the input/output schemas for the inference API to ensure
type safety and validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict


class IrisFeatures(BaseModel):
    """Input features for iris classification."""
    
    sepal_length: float = Field(..., description="Sepal length in cm", ge=0, le=10)
    sepal_width: float = Field(..., description="Sepal width in cm", ge=0, le=10)
    petal_length: float = Field(..., description="Petal length in cm", ge=0, le=10)
    petal_width: float = Field(..., description="Petal width in cm", ge=0, le=10)
    
    @field_validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    @classmethod
    def validate_positive(cls, v):
        """Ensure all measurements are positive."""
        if v < 0:
            raise ValueError("Measurements must be non-negative")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }


class InferenceRequest(BaseModel):
    """Request body for inference endpoint."""
    
    features: IrisFeatures
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                }
            }
        }


class InferenceResponse(BaseModel):
    """Response body for inference endpoint."""
    
    prediction: int = Field(..., description="Predicted class (0=setosa, 1=versicolor, 2=virginica)")
    prediction_label: str = Field(..., description="Human-readable class name")
    confidence: float = Field(..., description="Prediction confidence (0-1)", ge=0, le=1)
    model_version: str = Field(..., description="Model version used for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 0,
                "prediction_label": "setosa",
                "confidence": 0.95,
                "model_version": "1"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    model_loaded: bool
    model_version: str = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_version": "1"
            }
        }


class ContractResponse(BaseModel):
    """API contract information."""
    
    input_schema: Dict
    output_schema: Dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "features": {
                            "type": "object",
                            "properties": {
                                "sepal_length": {"type": "number"},
                                "sepal_width": {"type": "number"},
                                "petal_length": {"type": "number"},
                                "petal_width": {"type": "number"}
                            }
                        }
                    }
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "prediction": {"type": "integer"},
                        "prediction_label": {"type": "string"},
                        "confidence": {"type": "number"},
                        "model_version": {"type": "string"}
                    }
                }
            }
        }
