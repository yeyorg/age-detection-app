import time

from fastapi import APIRouter, Depends, File, Request, UploadFile

from age_detection_service.api.dependencies import get_model_service
from age_detection_service.api.schemas.common import ProbabilityItem
from age_detection_service.api.schemas.predict import PredictionResponse
from age_detection_service.core.image_processing import decode_and_validate_image
from age_detection_service.core.model_service import ModelService

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_age(
    request: Request,
    image: UploadFile = File(...),
    model_service: ModelService = Depends(get_model_service),
):
    """Predicción de rango de edad a partir de una imagen facial."""
    pil_image = await decode_and_validate_image(image)

    start = time.perf_counter()
    label, confidence, scores = model_service.predict(pil_image)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return PredictionResponse(
        request_id=request.state.request_id,
        predicted_age_range=label,
        confidence_percent=round(confidence, 2),
        all_probabilities=[
            ProbabilityItem(age_range=k, confidence_percent=round(v, 2))
            for k, v in scores.items()
        ],
        filename=image.filename or "unknown",
        inference_time_ms=round(elapsed_ms, 2),
    )
