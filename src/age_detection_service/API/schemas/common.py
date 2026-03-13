from pydantic import BaseModel, Field


class ProbabilityItem(BaseModel):
    """
    Representa la probabilidad asociada a un rango de edad específico.

    Este modelo se utiliza dentro de las respuestas de predicción para
    describir la confianza del modelo en cada una de las clases posibles
    de edad.

    Cada instancia de este esquema corresponde a un rango de edad y al
    porcentaje de probabilidad que el modelo asigna a ese rango durante
    el proceso de inferencia.

    Attributes:
        age_range (str):
            Rango de edad evaluado por el modelo (por ejemplo: "Edad 21-30").

        confidence_percent (float):
            Porcentaje de confianza que el modelo asigna a ese rango de edad.
            Este valor se encuentra restringido entre 0 y 100.
    """

    age_range: str = Field(..., description="Rango de edad")
    confidence_percent: float = Field(
        ..., ge=0, le=100, description="Confianza en porcentaje"
    )


class ErrorResponse(BaseModel):
    """
    Esquema estandarizado de respuesta para errores en la API.

    Este modelo define el formato uniforme utilizado por la API para
    devolver errores. Permite que los clientes consuman respuestas de
    error de forma consistente, independientemente del endpoint donde
    ocurra la excepción.

    Attributes:
        request_id (str):
            Identificador único de la solicitud HTTP. Permite correlacionar
            el error con los registros del sistema.

        error_code (str):
            Código interno de error definido por la aplicación. Este valor
            permite clasificar el tipo de error de forma estructurada.

        message (str):
            Mensaje legible que describe el error ocurrido.

        details (list[str] | None):
            Lista opcional de detalles adicionales que pueden proporcionar
            información más específica sobre el error. Puede ser `None`
            si no existen detalles adicionales.
    """

    request_id: str = Field(..., description="ID único de la petición")
    error_code: str = Field(..., description="Código de error interno")
    message: str = Field(..., description="Mensaje legible del error")
    details: list[str] | None = Field(
        default=None, description="Detalles adicionales del error"
    )
