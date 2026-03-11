from pydantic import BaseModel, Field

from age_detection_service.api.schemas.predict import PredictionResponse


class UserSummary(BaseModel):
    """Resumen de datos del usuario en la verificación."""

    nombre: str
    edad_calculada: int
    fecha_nacimiento: str


class VerificationResponse(BaseModel):
    """Respuesta de verificación completa (predicción + mayoría de edad)."""

    request_id: str = Field(..., description="ID único de la petición")
    prediction: PredictionResponse = Field(..., description="Resultado de predicción")
    is_adult: bool = Field(..., description="Si el modelo predice mayoría de edad")
    user_summary: UserSummary = Field(..., description="Resumen de datos del usuario")
