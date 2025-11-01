"""
Training script with MLflow experiment tracking.

This script:
1. Loads the Iris dataset
2. Trains a Random Forest classifier
3. Logs parameters, metrics, and the model to MLflow
4. Registers the model in MLflow Model Registry
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
import mlflow
import mlflow.sklearn


def load_data(data_path: str = "mlops-demo/data/raw/iris.csv"):
    """Load the Iris dataset from CSV."""
    print(f"📂 Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Encode target labels
    species_map = {"setosa": 0, "versicolor": 1, "virginica": 2}
    df["target"] = df["species"].map(species_map)
    
    # Features and target
    X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
    y = df["target"].values
    
    print(f"✅ Loaded {len(df)} samples with {X.shape[1]} features")
    return X, y, df


def train_model(X_train, y_train, n_estimators=100, max_depth=5, random_state=42):
    """Train a Random Forest classifier."""
    print(f"🌲 Training Random Forest (n_estimators={n_estimators}, max_depth={max_depth})...")
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    
    model.fit(X_train, y_train)
    print("✅ Model trained successfully")
    
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the model and return metrics."""
    print("📊 Evaluating model...")
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    
    print(f"✅ Accuracy: {accuracy:.4f}")
    print(f"✅ F1 Score: {f1:.4f}")
    
    # Print classification report
    target_names = ["setosa", "versicolor", "virginica"]
    print("\n" + classification_report(y_test, y_pred, target_names=target_names))
    
    return accuracy, f1


def main():
    """Main training pipeline with MLflow tracking."""
    
    # Set MLflow experiment
    experiment_name = "iris-classification"
    mlflow.set_experiment(experiment_name)
    print(f"🔬 MLflow Experiment: {experiment_name}")
    
    # Hyperparameters
    n_estimators = 100
    max_depth = 5
    random_state = 42
    test_size = 0.2
    
    # Start MLflow run
    with mlflow.start_run(run_name="random_forest_baseline"):
        
        # Load data
        X, y, df = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"📊 Train size: {len(X_train)}, Test size: {len(X_test)}")
        
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("n_samples", len(X))
        mlflow.log_param("n_features", X.shape[1])
        
        # Train model
        model = train_model(X_train, y_train, n_estimators, max_depth, random_state)
        
        # Evaluate model
        accuracy, f1 = evaluate_model(model, X_test, y_test)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        
        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="iris_classifier"
        )
        
        # Log tags
        mlflow.set_tag("dataset", "iris")
        mlflow.set_tag("framework", "scikit-learn")
        mlflow.set_tag("algorithm", "RandomForest")
        
        # Get run info
        run_id = mlflow.active_run().info.run_id
        print(f"\n🎯 MLflow Run ID: {run_id}")
        print("📁 Artifacts logged to: mlruns/")
        print("\n🚀 View results: mlflow ui")
        print("   Then navigate to: http://localhost:5000")
        
        return model, run_id


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting MLOps Training Pipeline")
    print("=" * 60)
    
    model, run_id = main()
    
    print("\n" + "=" * 60)
    print("✨ Training complete! Next steps:")
    print("=" * 60)
    print("1. View experiments: mlflow ui")
    print("2. Start inference service: uvicorn src.app:app --reload")
    print("3. Run tests: pytest tests/")
    print("=" * 60)
