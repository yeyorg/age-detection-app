import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from age_detection_service.api.schemas.common import ErrorResponse

logger = logging.getLogger("age_detection_service")


def register_error_handlers(app: FastAPI) -> None:
    """Registra manejadores de excepciones globales en la app FastAPI."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
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
    mapping = {
        400: "VALIDATION_ERROR",
        422: "UNPROCESSABLE_ENTITY",
        503: "MODEL_NOT_READY",
    }
    return mapping.get(status_code, "INTERNAL_ERROR")
