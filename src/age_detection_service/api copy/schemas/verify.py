from pydantic import BaseModel, Field

from age_detection_service.api.schemas.predict import PredictionResponse


class UserSummary(BaseModel):
    """
    Modelo que representa un resumen de la información del usuario.

    Este esquema se utiliza dentro de la respuesta del endpoint de verificación
    para incluir información relevante del usuario que fue utilizada durante
    el proceso de validación.

    Attributes:
        nombre (str):
            Nombre completo del usuario ingresado en el formulario.

        edad_calculada (int):
            Edad calculada a partir de la fecha de nacimiento proporcionada.

        fecha_nacimiento (str):
            Fecha de nacimiento del usuario en formato ISO (YYYY-MM-DD).
    """

    nombre: str
    edad_calculada: int
    fecha_nacimiento: str


class VerificationResponse(BaseModel):
    """
    Esquema de respuesta para el endpoint de verificación de edad.

    Este modelo encapsula el resultado completo del proceso de verificación,
    combinando:

        - El resultado de la predicción del modelo de detección de edad.
        - La determinación de si el usuario es mayor de edad.
        - Un resumen de los datos del usuario utilizados en la validación.

    Attributes:
        request_id (str):
            Identificador único de la solicitud HTTP. Este valor permite
            rastrear la petición en logs y sistemas de monitoreo.

        prediction (PredictionResponse):
            Resultado detallado de la predicción generada por el modelo
            de detección de edad.

        is_adult (bool):
            Indica si el rango de edad predicho por el modelo corresponde
            a una persona mayor de edad.

        user_summary (UserSummary):
            Resumen de los datos del usuario que fueron utilizados durante
            el proceso de verificación.
    """

    request_id: str = Field(..., description="ID único de la petición")
    prediction: PredictionResponse = Field(..., description="Resultado de predicción")
    is_adult: bool = Field(..., description="Si el modelo predice mayoría de edad")
    user_summary: UserSummary = Field(..., description="Resumen de datos del usuario")