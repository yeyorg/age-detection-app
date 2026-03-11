"""Validate the model loaded from MLflow Registry produces correct predictions.

This module retrieves a registered age-detection model from the MLflow Model Registry
and validates its functionality by:
    - Loading the model from the registry
    - Running inference on a dummy image
    - Measuring model load time and inference latency
    - Logging validation metrics back to MLflow

This is primarily used as a smoke test to confirm the registered model artifact is
functional and loads correctly from the registry.

Main workflow:
    1. Initialize MLflow tracking
    2. Fetch latest model version from Registry
    3. Load model and measure load time
    4. Run inference on dummy image and measure latency
    5. Log validation metrics to MLflow
    6. Print validation summary
"""

import time

import mlflow
import mlflow.transformers
from PIL import Image

REGISTERED_MODEL_NAME = "age-detection-model"


def predict_with_pipeline(pipeline, image: Image.Image):
    """Run prediction using the MLflow-loaded transformers pipeline.

    Takes a PIL image, runs it through the transformers pipeline, and extracts the
    predicted label and confidence score from the top result.

    Args:
        pipeline: transformers pipeline object loaded by MLflow, configured for
                  image classification.
        image (Image.Image): PIL Image object to classify.

    Returns:
        Tuple[str, float]: A tuple containing:
            - label (str): The predicted age category label
            - confidence (float): The prediction confidence as a percentage (0-100)

    Note:
        The confidence score from the pipeline (0-1) is converted to percentage.
    """
    results = pipeline(image)
    top = max(results, key=lambda r: r["score"])
    return top["label"], top["score"] * 100


def main():
    """Load model from registry, validate functionality, and log metrics to MLflow.

    Performs the following validation steps:
        1. Sets up MLflow tracking
        2. Constructs model URI for latest version from registry
        3. Loads transformers pipeline from registry and measures load time
        4. Creates dummy image (224x224) for testing
        5. Runs inference and measures inference time
        6. Extracts predicted label and confidence
        7. Creates new MLflow run and logs validation metrics

    Global variables used:
        REGISTERED_MODEL_NAME: Name of model to validate ("age-detection-model")

    Returns:
        None. Validation metrics logged to MLflow and summary printed.

    Prints:
        Model load time, prediction result, inference latency, and validation completion.

    Raises:
        Any exception from model loading or inference will propagate.
    """
    mlflow.set_tracking_uri("mlruns")

    model_uri = f"models:/{REGISTERED_MODEL_NAME}/latest"
    print(f"Loading model from: {model_uri}")

    start = time.perf_counter()
    pipeline = mlflow.transformers.load_model(model_uri)
    load_time = time.perf_counter() - start
    print(f"Model loaded in {load_time:.2f}s")

    # Create a dummy image for validation
    dummy_image = Image.new("RGB", (224, 224), color=(128, 128, 128))

    start = time.perf_counter()
    label, confidence = predict_with_pipeline(pipeline, dummy_image)
    inference_time = time.perf_counter() - start

    print(f"Prediction: {label} ({confidence:.2f}%)")
    print(f"Inference time: {inference_time:.4f}s")

    # Log validation metrics
    with mlflow.start_run(run_name="validate-registry-model"):
        mlflow.log_metrics(
            {
                "load_time_s": load_time,
                "inference_time_s": inference_time,
                "top_confidence": confidence,
            }
        )
        mlflow.log_param("predicted_label", label)

    print("Validation complete.")


if __name__ == "__main__":
    main()
