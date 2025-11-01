"""
FastAPI inference service for Iris classification.

This service:
1. Loads a trained model from MLflow
2. Exposes REST API endpoints for prediction
3. Provides contract validation
4. Includes health checks
"""

import os
import mlflow
import mlflow.sklearn
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

from infer_schema import (
    InferenceRequest,
    InferenceResponse,
    HealthResponse,
    ContractResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Iris Classification API",
    description="MLOps demo: Inference service for Iris flower classification",
    version="1.0.0"
)

# Global model variable
model = None
model_version = None

# Species mapping
SPECIES_MAP = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}


def load_model_from_mlflow():
    """
    Load the latest registered model from MLflow Model Registry.
    Falls back to loading from the latest run if registry is not available.
    """
    global model, model_version
    
    try:
        # Try to load from Model Registry (production stage)
        model_name = "iris_classifier"
        
        try:
            model_uri = f"models:/{model_name}/latest"
            logger.info(f"Loading model from registry: {model_uri}")
            model = mlflow.sklearn.load_model(model_uri)
            model_version = "latest"
            logger.info(f"✅ Model loaded from registry: {model_name}")
        except Exception as registry_error:
            logger.warning(f"Failed to load from registry: {registry_error}")
            
            # Fallback: Load from latest run
            logger.info("Attempting to load model from latest run...")
            
            # Find the latest run in the experiment
            experiment_name = "iris-classification"
            experiment = mlflow.get_experiment_by_name(experiment_name)
            
            if experiment is None:
                raise Exception(f"Experiment '{experiment_name}' not found. Please run train.py first.")
            
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["start_time DESC"],
                max_results=1
            )
            
            if len(runs) == 0:
                raise Exception("No runs found in experiment. Please run train.py first.")
            
            run_id = runs.iloc[0]["run_id"]
            model_uri = f"runs:/{run_id}/model"
            logger.info(f"Loading model from run: {run_id}")
            
            model = mlflow.sklearn.load_model(model_uri)
            model_version = run_id[:7]  # Short run ID
            logger.info(f"✅ Model loaded from run: {run_id}")
            
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise


# Load model on startup
@app.on_event("startup")
async def startup_event():
    """Load model when the service starts."""
    logger.info("🚀 Starting Iris Classification Service...")
    
    # Set MLflow tracking URI (default: local mlruns folder)
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    logger.info(f"📊 MLflow tracking URI: {mlflow_tracking_uri}")
    
    try:
        load_model_from_mlflow()
        logger.info("✅ Service ready for predictions")
    except Exception as e:
        logger.error(f"❌ Service startup failed: {e}")
        # Don't crash the service, but model won't be available
        pass


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Iris Classification API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "contract": "/contract",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    if model is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "model_loaded": False,
                "model_version": None
            }
        )
    
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_version=model_version
    )


@app.get("/contract", response_model=ContractResponse, tags=["Contract"])
async def get_contract():
    """Get the API contract (input/output schemas)."""
    return ContractResponse(
        input_schema=InferenceRequest.model_json_schema(),
        output_schema=InferenceResponse.model_json_schema()
    )


@app.post("/predict", response_model=InferenceResponse, tags=["Prediction"])
async def predict(request: InferenceRequest):
    """
    Make a prediction on iris features.
    
    Args:
        request: InferenceRequest with iris features
        
    Returns:
        InferenceResponse with prediction, label, confidence, and model version
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service is unavailable."
        )
    
    try:
        # Extract features
        features = request.features
        X = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Make prediction
        prediction = int(model.predict(X)[0])
        
        # Get confidence (probability of predicted class)
        probabilities = model.predict_proba(X)[0]
        confidence = float(probabilities[prediction])
        
        # Get label
        prediction_label = SPECIES_MAP.get(prediction, "unknown")
        
        logger.info(
            f"Prediction: {prediction_label} (class={prediction}, confidence={confidence:.4f})"
        )
        
        return InferenceResponse(
            prediction=prediction,
            prediction_label=prediction_label,
            confidence=confidence,
            model_version=model_version
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
