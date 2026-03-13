import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from age_detection_service.api.schemas.common import ErrorResponse

logger = logging.getLogger("age_detection_service")


def register_error_handlers(app: FastAPI) -> None:
    """
    Registra los manejadores globales de excepciones para la aplicación FastAPI.

    Esta función centraliza el tratamiento de errores no controlados y de
    excepciones HTTP dentro de la aplicación. Su objetivo es garantizar
    que todas las respuestas de error tengan un formato consistente,
    estructurado y alineado con el esquema `ErrorResponse`.


    Además, ambos manejadores intentan recuperar el identificador de la
    solicitud (`request_id`) desde `request.state`, lo que facilita la
    trazabilidad y depuración de errores en logs y respuestas.

    Args:
        app (FastAPI):
            Instancia de la aplicación FastAPI sobre la cual se registrarán
            los manejadores globales de excepciones.

    Returns:
        None.

    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """
        Maneja excepciones HTTP generadas explícitamente dentro de la aplicación.

        Este manejador intercepta excepciones del tipo `HTTPException` y
        construye una respuesta JSON estructurada basada en el esquema
        `ErrorResponse`. El código interno de error se obtiene a partir del
        código de estado HTTP usando la función `_status_to_error_code`.

        Args:
            request (Request):
                Objeto de solicitud HTTP recibido por FastAPI. Se utiliza
                para recuperar información contextual, como el `request_id`
                almacenado en `request.state`.

            exc (HTTPException):
                Excepción HTTP capturada. Contiene el código de estado
                (`status_code`) y el detalle del error (`detail`).

        Returns:
            JSONResponse:
                Respuesta JSON estructurada con:
                - `request_id`: identificador de la solicitud.
                - `error_code`: código interno derivado del estado HTTP.
                - `message`: mensaje de error contenido en `exc.detail`.
        """
        request_id = getattr(request.state, "request_id", "unknown")
        error_code = _status_to_error_code(exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                request_id=request_id,
                error_code=error_code,
                message=str(exc.detail),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Maneja cualquier excepción no controlada ocurrida en la aplicación.

        Este manejador actúa como mecanismo de respaldo para errores no previstos
        que no correspondan a una `HTTPException`. Cuando ocurre una excepción
        de este tipo se registra un mensaje de error en los logs con el nivel de severidad
        "exception", lo que incluye el traceback completo. Luego, se retorna una respuesta 
        JSON con código de estado 500 y un mensaje genérico de error interno.

        Args:
            request (Request):
                Objeto de solicitud HTTP recibido por FastAPI. Se utiliza
                para obtener el `request_id` asociado a la petición actual.

            exc (Exception):
                Excepción genérica capturada por el manejador global.

        Returns:
            JSONResponse:
                Respuesta JSON con código de estado 500 y estructura
                compatible con `ErrorResponse`.
        """
        request_id = getattr(request.state, "request_id", "unknown")
        logger.exception("Unhandled error [request_id=%s]", request_id)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                request_id=request_id,
                error_code="INTERNAL_ERROR",
                message="Error interno del servidor",
            ).model_dump(),
        )


def _status_to_error_code(status_code: int) -> str:
    """
    Convierte un código de estado HTTP en un código interno de error.

    Esta función se utiliza para mapear códigos de estado HTTP a códigos
    de error semánticos definidos por la aplicación. Esto permite
    estandarizar la respuesta de errores y desacoplar la representación
    interna de errores del simple código HTTP.

    Mapeos definidos:
        - 400 -> "VALIDATION_ERROR"
        - 422 -> "UNPROCESSABLE_ENTITY"
        - 503 -> "MODEL_NOT_READY"

    Si el código recibido no está definido en el mapeo, la función retorna
    por defecto `"INTERNAL_ERROR"`.

    Args:
        status_code (int):
            Código de estado HTTP que se desea traducir a un código de error
            interno de la aplicación.

    Returns:
        str:
            Código interno de error asociado al `status_code` recibido.
    """
    mapping = {
        400: "VALIDATION_ERROR",
        422: "UNPROCESSABLE_ENTITY",
        503: "MODEL_NOT_READY",
    }
    return mapping.get(status_code, "INTERNAL_ERROR")
