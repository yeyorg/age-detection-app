"""Servicio de carga e inferencia del modelo de detección de edad.

Encapsula la lógica de carga del modelo preentrenado de Hugging Face
y la ejecución de predicciones sobre imágenes faciales.
"""

import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

from age_detection_service.config import MODEL_NAME, ID2LABEL


class ModelService:
    """Servicio de estilo Singleton que se encarga de la carga y la inferencia de modelos."""

    def __init__(self):
        """Inicializa el servicio sin cargar el modelo.

        El modelo y el procesador se cargan de forma diferida
        al invocar el método ``load`` o al realizar la primera predicción.
        """
        self._processor = None
        self._model = None

    @property
    def is_loaded(self) -> bool:
        """Indica si el modelo ya fue cargado en memoria."""
        return self._model is not None

    def load(self):
        """Carga el procesador de imágenes y el modelo desde Hugging Face.

        Si el modelo ya está cargado, la operación es idempotente.
        Al finalizar, el modelo se coloca en modo evaluación.
        """
        if self.is_loaded:
            return
        self._processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        self._model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
        self._model.eval()

    def predict(self, image: Image.Image) -> tuple[str, float, dict[str, float]]:
        """Ejecuta la predicción de rango de edad sobre una imagen.

        Args:
            image: Imagen PIL a clasificar.

        Returns:
            Tupla con la etiqueta predicha, la confianza en porcentaje
            y un diccionario con las probabilidades de cada clase.
        """
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
