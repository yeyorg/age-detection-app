from pydantic import BaseModel, Field


class ProbabilityItem(BaseModel):
    """Probabilidad por rango de edad."""

    age_range: str = Field(..., description="Rango de edad")
    confidence_percent: float = Field(
        ..., ge=0, le=100, description="Confianza en porcentaje"
    )


class ErrorResponse(BaseModel):
    """Respuesta estandarizada de error."""

    request_id: str = Field(..., description="ID único de la petición")
    error_code: str = Field(..., description="Código de error interno")
    message: str = Field(..., description="Mensaje legible del error")
    details: list[str] | None = Field(
        default=None, description="Detalles adicionales del error"
    )
