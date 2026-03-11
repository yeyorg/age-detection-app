from fastapi import HTTPException, Request

from age_detection_service.core.model_service import ModelService


def get_model_service(request: Request) -> ModelService:
    """Dependency injection: obtiene el ModelService del app state."""
    service: ModelService = request.app.state.model_service
    if not service.is_loaded:
        raise HTTPException(503, detail="Modelo no disponible aún")
    return service
