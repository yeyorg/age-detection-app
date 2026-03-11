"""Register the HuggingFace age-detection model in MLflow Model Registry.

This module loads a pre-trained Siglip image classification model and registers it in the
MLflow Model Registry. During registration, key metrics are collected:
    - Model load time
    - Dummy inference time (using a synthetic 224x224 image)
    - Model confidence on dummy inference
    - Total number of model parameters

These metrics provide baseline performance indicators for the registered model.

Main workflow:
    1. Initialize MLflow tracking and experiment
    2. Load Siglip model and image processor
    3. Measure model loading time and inference latency
    4. Register model in MLflow Model Registry
    5. Log parameters and metrics
    6. Display registration summary
"""

import time

import mlflow
import mlflow.transformers
import torch
from PIL import Image
from transformers import AutoImageProcessor, SiglipForImageClassification

from age_detection_service.config import ID2LABEL, MODEL_NAME

EXPERIMENT_NAME = "age-detection"
REGISTERED_MODEL_NAME = "age-detection-model"


def main():
    """Load model, collect performance metrics, and register in MLflow Model Registry.

    Performs the following steps:
        1. Sets up MLflow tracking and experiment
        2. Loads pre-trained Siglip model and image processor
        3. Measures model loading time
        4. Runs dummy inference to measure latency and confidence
        5. Counts total model parameters
        6. Creates MLflow run and logs metrics/parameters
        7. Registers model in MLflow Model Registry

    Global variables used:
        EXPERIMENT_NAME: MLflow experiment name ("age-detection")
        REGISTERED_MODEL_NAME: Name for registered model ("age-detection-model")
        MODEL_NAME: Pre-trained model identifier from HuggingFace
        ID2LABEL: Mapping from model class indices to age labels

    Returns:
        None. Model is registered in MLflow and summary printed to console.

    Prints:
        Registration confirmation and performance metrics summary.

    Raises:
        Any exception from model loading or MLflow operations will propagate.
    """
    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment(EXPERIMENT_NAME)

    start = time.perf_counter()
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = SiglipForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    load_time = time.perf_counter() - start

    # Run a dummy inference to measure latency
    dummy = Image.new("RGB", (224, 224), color=(128, 128, 128))
    inputs = processor(images=dummy, return_tensors="pt")
    start = time.perf_counter()
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]
    inference_time = time.perf_counter() - start

    top_idx = torch.argmax(probs).item()
    top_confidence = float(probs[top_idx]) * 100
    num_params = sum(p.numel() for p in model.parameters())

    with mlflow.start_run(run_name="register-model"):
        mlflow.log_params(
            {
                "model_name": MODEL_NAME,
                "num_classes": len(ID2LABEL),
                "id2label": str(ID2LABEL),
            }
        )

        mlflow.log_metrics(
            {
                "model_load_time_s": load_time,
                "dummy_inference_time_s": inference_time,
                "dummy_top_confidence": top_confidence,
                "num_parameters": num_params,
            }
        )

        mlflow.transformers.log_model(
            transformers_model={"model": model, "image_processor": processor},
            artifact_path="model",
            registered_model_name=REGISTERED_MODEL_NAME,
            task="image-classification",
        )

    print(f"Model registered as '{REGISTERED_MODEL_NAME}' in MLflow.")
    print(f"  Load time: {load_time:.2f}s | Inference: {inference_time:.4f}s")
    print(f"  Parameters: {num_params:,} | Dummy confidence: {top_confidence:.2f}%")


if __name__ == "__main__":
    main()
