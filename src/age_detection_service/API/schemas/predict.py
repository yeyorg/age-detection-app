from pydantic import BaseModel, Field

from age_detection_service.api.schemas.common import ProbabilityItem


class PredictionResponse(BaseModel):
    """Respuesta de predicción de edad."""

    request_id: str = Field(..., description="ID único de la petición")
    predicted_age_range: str = Field(..., description="Rango de edad predicho")
    confidence_percent: float = Field(
        ..., ge=0, le=100, description="Confianza principal"
    )
    all_probabilities: list[ProbabilityItem] = Field(
        ..., description="Probabilidades por clase"
    )
    filename: str = Field(..., description="Nombre del archivo procesado")
    inference_time_ms: float = Field(
        ..., description="Tiempo de inferencia en milisegundos"
    )
