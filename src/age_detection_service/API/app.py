import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from age_detection_service.api.middleware.error_handler import register_error_handlers
from age_detection_service.api.middleware.logging_middleware import LoggingMiddleware
from age_detection_service.api.middleware.request_id import RequestIdMiddleware
from age_detection_service.api.routers import health, model_info, predict, verify
from age_detection_service.core.model_service import ModelService

logger = logging.getLogger("age_detection_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo al arrancar y libera recursos al parar."""
    logger.info("Cargando modelo de detección de edad...")
    app.state.model_service.load()
    logger.info("Modelo cargado exitosamente.")
    yield


def create_app() -> FastAPI:
    """Application factory — construye y configura la app FastAPI."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )

    app = FastAPI(
        title="Age Detection API",
        description="Predicción de edad facial con modelo de Hugging Face",
        version="1.0.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan,
    )

    # -- State --
    app.state.model_service = ModelService()

    # -- Middleware (orden inverso de ejecución) --
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -- Error handlers --
    register_error_handlers(app)

    # -- Routers --
    prefix = "/api/v1"
    app.include_router(health.router, prefix=prefix, tags=["health"])
    app.include_router(predict.router, prefix=prefix, tags=["prediction"])
    app.include_router(verify.router, prefix=prefix, tags=["verification"])
    app.include_router(model_info.router, prefix=prefix, tags=["model"])

    return app


app = create_app()
