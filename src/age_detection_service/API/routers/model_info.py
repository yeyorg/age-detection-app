from fastapi import APIRouter

from age_detection_service.config import ID2LABEL, MODEL_NAME

router = APIRouter()


@router.get("/model/metadata")
async def model_metadata():
    """Información del modelo cargado (clases, nombre, labels)."""
    return {
        "model_name": MODEL_NAME,
        "num_classes": len(ID2LABEL),
        "labels": ID2LABEL,
    }
