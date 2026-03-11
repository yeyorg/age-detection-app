from pydantic import BaseModel, Field
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io
import uvicorn
import traceback


class ProbabilityItem(BaseModel):
    """Estructura de probabilidad por rango de edad."""

    age_range: str = Field(..., description="Rango de edad")
    confidence_percent: float = Field(
        ..., ge=0, le=100, description="Confianza en porcentaje"
    )


class PredictionResponse(BaseModel):
    """Respuesta completa de prediccion de edad."""

    predicted_age_range: str = Field(..., description="Rango de edad predicho")
    confidence_percent: float = Field(
        ..., ge=0, le=100, description="Confianza principal"
    )
    all_probabilities: List[ProbabilityItem] = Field(
        ..., description="Probabilidades por clase"
    )
    success: bool = Field(default=True)
    filename: str = Field(..., description="Nombre del archivo")


MODEL_NAME = "prithivMLmods/facial-age-detection"
ID2LABEL = {
    0: "Edad 01-10",
    1: "Edad 11-20",
    2: "Edad 21-30",
    3: "Edad 31-40",
    4: "Edad 41-55",
    5: "Edad 56-65",
    6: "Edad 66-80",
    7: "Edad 80+",
}

app = FastAPI(
    title="Age Detection API",
    description="Prediccion de edad facial con modelo de Hugging Face",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

processor = None
model = None


def load_model():
    """Carga el modelo de Hugging Face."""
    global processor, model
    if model is None:
        processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
        model.eval()
    return processor, model


@app.post("/predict", response_model=PredictionResponse)
async def predict_age(image: UploadFile = File(...)):
    """
    Prediccion de edad facial.

    Args:
        image: Imagen JPG/PNG del rostro

    Returns:
        PredictionResponse con rango de edad y probabilidades

    Raises:
        HTTPException: Error de validacion o prediccion
    """
    try:
        if not image.content_type.startswith("image/"):
            raise HTTPException(400, "Solo imagenes JPG/PNG")

        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

        processor, model = load_model()
        inputs = processor(images=pil_image, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]

        top_idx = torch.argmax(probs).item()
        label = ID2LABEL[top_idx]
        confidence = float(probs[top_idx]) * 100

        probabilities = [
            ProbabilityItem(
                age_range=ID2LABEL[i],
                confidence_percent=round(float(probs[i]) * 100, 2),
            )
            for i in range(len(probs))
        ]

        return PredictionResponse(
            predicted_age_range=label,
            confidence_percent=round(confidence, 2),
            all_probabilities=probabilities,
            filename=image.filename,
        )
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(500, f"Error de prediccion: {str(e)}")


@app.get("/")
async def root():
    """
    Estado general de la API.

    Returns:
        Informacion del modelo y endpoints disponibles
    """
    return {"message": "Age Detection API", "model": MODEL_NAME, "endpoint": "/predict"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
