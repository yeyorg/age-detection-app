import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("age_detection_service")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware encargado de registrar información de cada solicitud HTTP procesada por la API.

    Este middleware intercepta todas las peticiones entrantes a la aplicación
    FastAPI y registra información relevante para monitoreo y depuración.

    El tiempo de ejecución de la solicitud se calcula utilizando
    `time.perf_counter`, lo que permite medir con alta precisión la
    duración del procesamiento del request.

    Hereda de:
        BaseHTTPMiddleware (Starlette), lo que permite interceptar el
        ciclo completo de la solicitud antes y después de que sea
        procesada por los endpoints.

    Notes:
        - El `request_id` puede ser agregado previamente por otro middleware
          dedicado a la generación de identificadores de solicitud.
        - Si no existe `request.state.request_id`, se utilizará el valor "-".
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        request_id = getattr(request.state, "request_id", "-")
        logger.info(
            "%s %s -> %s (%.1fms) [request_id=%s]",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            request_id,
        )
        return response
