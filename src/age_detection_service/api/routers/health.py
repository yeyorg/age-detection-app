from datetime import datetime, timezone

from fastapi import APIRouter, Request

from age_detection_service.config import MODEL_NAME

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    """
    Endpoint de verificación de estado del servicio (health check).

    Este endpoint permite comprobar si la API está funcionando correctamente
    y si el modelo de detección de edad se encuentra cargado y disponible
    para realizar inferencias.

    La información retornada incluye el estado general del servicio,
    el estado del modelo de inferencia, el nombre del modelo utilizado,
    la versión de la aplicación y una marca temporal en formato UTC.

    Args:
        request (Request):
            Objeto de solicitud HTTP proporcionado por FastAPI.
            Se utiliza para acceder al estado global de la aplicación
            (`request.app.state`) donde se encuentra almacenada la
            instancia del servicio de modelo (`model_service`).

    Returns:
        dict:
            Diccionario con la información de estado del sistema:

            - status (str):
                Estado general del servicio. Puede ser:
                    * "healthy" si el modelo está cargado.
                    * "degraded" si el modelo aún no está disponible.

            - model_loaded (bool):
                Indica si el modelo de inferencia se encuentra cargado
                y listo para procesar solicitudes.

            - model_name (str):
                Nombre del modelo utilizado por el sistema.

            - version (str):
                Versión actual de la aplicación definida en `app.version`.

            - timestamp (str):
                Marca temporal de la respuesta en formato ISO 8601
                usando la zona horaria UTC.

    Notes:
        - Este endpoint no realiza inferencia ni carga de modelo.
        - El estado del modelo se obtiene directamente desde
          `request.app.state.model_service`.
        - La marca temporal se genera utilizando `datetime.now(timezone.utc)`.
    """
    model_service = request.app.state.model_service
    return {
        "status": "healthy" if model_service.is_loaded else "degraded",
        "model_loaded": model_service.is_loaded,
        "model_name": MODEL_NAME,
        "version": request.app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
