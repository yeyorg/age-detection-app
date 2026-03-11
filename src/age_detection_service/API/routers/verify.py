import time
from datetime import date

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

from age_detection_service.api.dependencies import get_model_service
from age_detection_service.api.schemas.common import ProbabilityItem
from age_detection_service.api.schemas.predict import PredictionResponse
from age_detection_service.api.schemas.verify import (
    UserSummary,
    VerificationResponse,
)
from age_detection_service.core.age_verification import (
    es_mayor_segun_prediccion,
    validar_formulario,
)
from age_detection_service.core.image_processing import decode_and_validate_image
from age_detection_service.core.model_service import ModelService

router = APIRouter()


@router.post("/verify", response_model=VerificationResponse)
async def verify_age(
    request: Request,
    image: UploadFile = File(...),
    nombre: str = Form(..., min_length=3),
    genero: str = Form(...),
    cedula: str = Form(...),
    fecha_nacimiento: date = Form(...),
    model_service: ModelService = Depends(get_model_service),
):
    """Verificación completa: predicción + validación de mayoría de edad."""
    errores, edad = validar_formulario(nombre, genero, cedula, fecha_nacimiento)
    if errores:
        from fastapi import HTTPException

        raise HTTPException(400, detail="; ".join(errores))

    pil_image = await decode_and_validate_image(image)

    start = time.perf_counter()
    label, confidence, scores = model_service.predict(pil_image)
    elapsed_ms = (time.perf_counter() - start) * 1000

    prediction = PredictionResponse(
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

    return VerificationResponse(
        request_id=request.state.request_id,
        prediction=prediction,
        is_adult=es_mayor_segun_prediccion(label),
        user_summary=UserSummary(
            nombre=nombre.strip(),
            edad_calculada=edad,
            fecha_nacimiento=fecha_nacimiento.isoformat(),
        ),
    )
