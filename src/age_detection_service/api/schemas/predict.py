from pydantic import BaseModel, Field

from age_detection_service.api.schemas.common import ProbabilityItem


class PredictionResponse(BaseModel):
    """
    Esquema de respuesta para el endpoint de predicción de edad.

    Este modelo representa la estructura de datos devuelta por el endpoint
    `/predict`, el cual procesa una imagen facial y utiliza un modelo de
    machine learning para estimar el rango de edad de la persona en la imagen.

    La respuesta incluye información sobre la predicción principal, las
    probabilidades asociadas a cada rango de edad posible, el archivo
    procesado y el tiempo de inferencia del modelo.

    Attributes:
        request_id (str):
            Identificador único de la solicitud HTTP. Permite rastrear la
            petición en logs, sistemas de monitoreo o debugging.

        predicted_age_range (str):
            Rango de edad estimado por el modelo (por ejemplo: "Edad 21-30").

        confidence_percent (float):
            Porcentaje de confianza asociado a la predicción principal del
            modelo. Su valor está restringido entre 0 y 100.

        all_probabilities (list[ProbabilityItem]):
            Lista de probabilidades para cada rango de edad posible
            generado por el modelo. Cada elemento representa una clase
            y su nivel de confianza.

        filename (str):
            Nombre del archivo de imagen que fue procesado durante
            la inferencia.

        inference_time_ms (float):
            Tiempo total que tardó el modelo en procesar la imagen
            y generar la predicción, expresado en milisegundos.
    """

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