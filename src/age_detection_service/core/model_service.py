import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

from age_detection_service.config import MODEL_NAME, ID2LABEL


class ModelService:
    """Singleton-style service that owns model loading and inference."""

    def __init__(self):
        self._processor = None
        self._model = None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def load(self):
        if self.is_loaded:
            return
        self._processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        self._model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
        self._model.eval()

    def predict(self, image: Image.Image) -> tuple[str, float, dict[str, float]]:
        if not self.is_loaded:
            self.load()

        inputs = self._processor(images=image.convert("RGB"), return_tensors="pt")

        with torch.no_grad():
            probs = torch.softmax(self._model(**inputs).logits, dim=1)[0]

        top_idx = torch.argmax(probs).item()
        label = ID2LABEL[top_idx]
        confidence = float(probs[top_idx]) * 100
        scores = {ID2LABEL[i]: float(probs[i]) * 100 for i in range(len(probs))}
        return label, confidence, scores
