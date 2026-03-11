from datetime import datetime, timezone

from fastapi import APIRouter, Request

from age_detection_service.config import MODEL_NAME

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    """Estado del servicio y del modelo."""
    model_service = request.app.state.model_service
    return {
        "status": "healthy" if model_service.is_loaded else "degraded",
        "model_loaded": model_service.is_loaded,
        "model_name": MODEL_NAME,
        "version": request.app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
