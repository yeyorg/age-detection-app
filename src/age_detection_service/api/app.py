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
    """
    Gestiona el ciclo de vida de la aplicación FastAPI.

    Este contexto asincrónico se ejecuta automáticamente durante el
    arranque y apagado de la aplicación. Su objetivo principal es
    inicializar recursos necesarios antes de comenzar a atender
    solicitudes HTTP.


    Args:
        app (FastAPI):
            Instancia de la aplicación FastAPI que contiene el estado global
            de la aplicación, incluyendo el servicio de modelo almacenado en
            `app.state.model_service`.

    Yields:
        None:
            Permite que la aplicación continúe ejecutándose mientras
            el contexto permanece activo.
    """
    logger.info("Cargando modelo de detección de edad...")
    app.state.model_service.load()
    logger.info("Modelo cargado exitosamente.")
    yield


def create_app() -> FastAPI:
    """
    Crea y configura la instancia principal de la aplicación FastAPI.

    Esta función actúa como una *application factory*, responsable de
    construir la aplicación y registrar todos sus componentes:

        - Configuración de logging.
        - Inicialización del estado global de la aplicación.
        - Registro de middlewares.
        - Configuración de manejadores globales de errores.
        - Registro de routers de la API.

    Este patrón permite una mejor organización del proyecto y facilita
    la creación de instancias de la aplicación para testing o despliegue.

    Returns:
        FastAPI:
            Instancia completamente configurada de la aplicación FastAPI.
    """
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
