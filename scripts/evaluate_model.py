"""Evaluate the age-detection model on FairFace samples and log a confusion matrix.

This module loads the age-detection model (Siglip) and evaluates it on samples from the
FairFace dataset. Ground truth labels are mapped from FairFace age categories to the model's
age ranges. Predictions are made on the sampled images, and evaluation metrics (accuracy,
classification report, and confusion matrix) are computed and logged to MLflow.

The confusion matrix is also saved as a PNG visualization for visual inspection.

Main workflow:
    1. Load FairFace dataset samples
    2. Map age labels from FairFace format to model format
    3. Load the pre-trained Siglip model
    4. Run batch predictions
    5. Compute metrics (accuracy, confusion matrix, classification report)
    6. Log results and artifacts to MLflow
"""

import random
import time

import mlflow
import numpy as np
import torch
from datasets import load_dataset
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import AutoImageProcessor, SiglipForImageClassification

from age_detection_service.config import FAIRFACE_TO_MODEL, ID2LABEL, MODEL_NAME

EXPERIMENT_NAME = "age-detection"
N_SAMPLES = 200

MODEL_LABELS = list(ID2LABEL.values())


def predict_batch(processor, model, images):
    """Run predictions on a list of PIL images.

    Processes each image through the model using the provided processor, applies softmax
    to the logits, and returns the predicted age label for each image.

    Args:
        processor: AutoImageProcessor instance for preprocessing images.
        model: SiglipForImageClassification model for age classification.
        images: List of PIL Image objects to predict on.

    Returns:
        List[str]: Predicted age labels for each image, using the model's ID2LABEL mapping.

    Note:
        Predictions are run in no-grad mode (inference mode) for efficiency.
    """
    predictions = []
    for img in images:
        img = img.convert("RGB")
        inputs = processor(images=img, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]
        top_idx = torch.argmax(probs).item()
        predictions.append(ID2LABEL[top_idx])
    return predictions


def plot_confusion_matrix(cm, labels, output_path):
    """Save confusion matrix as a PNG image using matplotlib.

    Renders a heatmap-style confusion matrix with annotations showing the count at each cell.
    The background color intensity indicates the magnitude of values. The matrix is saved
    as a high-resolution PNG file.

    Args:
        cm: numpy.ndarray of shape (n_classes, n_classes), the confusion matrix.
        labels: List[str] of class labels for axis annotations.
        output_path: str, path where the PNG image will be saved.

    Returns:
        None. Saves the figure to output_path and prints confirmation message.

    Note:
        Uses matplotlib's 'Agg' backend for non-interactive rendering.
        Figure size is (10, 8) inches at 150 dpi.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="Real (FairFace)",
        xlabel="Predicho (Modelo)",
        title="Matriz de Confusión - Detección de Edad",
    )

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Annotate cells
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Confusion matrix saved to {output_path}")


def main():
    """Main evaluation pipeline: load dataset, predict, and log results to MLflow.

    Orchestrates the entire evaluation workflow:
        1. Sets up MLflow tracking and experiment
        2. Loads FairFace dataset and samples random images
        3. Maps FairFace age labels to model age labels
        4. Loads the pre-trained Siglip model
        5. Runs batch predictions on samples
        6. Computes evaluation metrics (accuracy, classification report, confusion matrix)
        7. Saves confusion matrix visualization
        8. Logs all metrics, parameters, and artifacts to MLflow

    Global variables used:
        EXPERIMENT_NAME: MLflow experiment name ("age-detection")
        N_SAMPLES: Number of random samples to load from FairFace (200)
        FAIRFACE_TO_MODEL: Mapping of FairFace age categories to model age ranges
        MODEL_LABELS: List of model's age category labels
        MODEL_NAME: Pre-trained model identifier
        ID2LABEL: Mapping from model class indices to age labels

    Returns:
        None. Results are logged to MLflow and visualizations saved to disk.

    Prints:
        Status messages about data loading, model loading, and inference progress.
        Accuracy, inference time statistics, and classification report.
    """
    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment(EXPERIMENT_NAME)

    print(f"Loading FairFace dataset (sampling {N_SAMPLES} images)...")
    dataset = load_dataset("HuggingFaceM4/FairFace", "1.25", split="train")

    # Get the age feature names from the dataset
    age_feature = dataset.features["age"]
    age_names = age_feature.names if hasattr(age_feature, "names") else None

    # Sample random indices
    indices = random.sample(range(len(dataset)), min(N_SAMPLES, len(dataset)))
    samples = dataset.select(indices)

    # Map ground truth labels
    images = []
    true_labels = []
    skipped = 0
    for row in samples:
        age_raw = row["age"]
        if age_names is not None:
            age_str = age_names[age_raw]
        else:
            age_str = str(age_raw)

        mapped = FAIRFACE_TO_MODEL.get(age_str)
        if mapped is None:
            skipped += 1
            continue
        true_labels.append(mapped)
        images.append(row["image"])

    print(f"Loaded {len(images)} images ({skipped} skipped due to unmapped labels)")

    # Load model
    print("Loading model...")
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = SiglipForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()

    # Predict
    print("Running predictions...")
    start = time.perf_counter()
    pred_labels = predict_batch(processor, model, images)
    total_time = time.perf_counter() - start
    avg_time = total_time / len(images) if images else 0

    # Metrics
    accuracy = accuracy_score(true_labels, pred_labels)
    report = classification_report(
        true_labels, pred_labels, labels=MODEL_LABELS, zero_division=0
    )
    cm = confusion_matrix(true_labels, pred_labels, labels=MODEL_LABELS)

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Total inference time: {total_time:.2f}s ({avg_time:.4f}s/image)")
    print(f"\nClassification Report:\n{report}")

    # Save confusion matrix plot
    cm_path = "confusion_matrix.png"
    plot_confusion_matrix(cm, MODEL_LABELS, cm_path)

    # Log to MLflow
    with mlflow.start_run(run_name="evaluate-fairface"):
        mlflow.log_params(
            {
                "dataset": "HuggingFaceM4/FairFace",
                "n_samples": len(images),
                "model_name": MODEL_NAME,
            }
        )
        mlflow.log_metrics(
            {
                "accuracy": accuracy,
                "total_inference_time_s": total_time,
                "avg_inference_time_s": avg_time,
                "n_evaluated": len(images),
            }
        )
        mlflow.log_artifact(cm_path, artifact_path="evaluation")
        mlflow.log_text(report, "evaluation/classification_report.txt")

        # Log confusion matrix as CSV
        import csv
        import io

        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([""] + MODEL_LABELS)
        for i, row_label in enumerate(MODEL_LABELS):
            writer.writerow([row_label] + [int(v) for v in cm[i]])
        mlflow.log_text(buf.getvalue(), "evaluation/confusion_matrix.csv")

    print("\nResults logged to MLflow experiment 'age-detection'.")


if __name__ == "__main__":
    main()
