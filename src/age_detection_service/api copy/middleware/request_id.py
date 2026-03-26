import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware que genera o propaga un identificador único de solicitud (Request ID).

    Este middleware se encarga de asegurar que cada petición HTTP que atraviesa
    la aplicación tenga asociado un identificador único (`request_id`). Dicho
    identificador se utiliza para mejorar la trazabilidad de las solicitudes
    dentro del sistema, especialmente en logs, monitoreo y depuración.

    Hereda de:
        BaseHTTPMiddleware (Starlette), lo que permite interceptar el flujo
        completo de las solicitudes HTTP dentro de la aplicación.

    Notes:
        - El identificador generado es un UUID versión 4.
        - Otros middlewares o componentes pueden acceder al identificador
          mediante `request.state.request_id`.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Procesa la solicitud HTTP y asigna un identificador único de request.

        Este método intercepta cada solicitud entrante, determina si existe
        un `X-Request-ID` en los encabezados y, en caso contrario, genera uno
        nuevo. El identificador se almacena en el estado de la solicitud
        (`request.state`) y posteriormente se incluye también en la respuesta.

        Args:
            request (Request):
                Objeto de solicitud HTTP entrante que contiene los datos
                de la petición, incluidos los encabezados y el estado
                asociado al request.

            call_next (RequestResponseEndpoint):
                Función que representa el siguiente paso en el pipeline
                de procesamiento de la solicitud (otro middleware o el
                endpoint final).

        Returns:
            Response:
                Respuesta HTTP generada por el endpoint o middleware
                posterior, con el encabezado `X-Request-ID` incluido.
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
