from fastapi import HTTPException, Request

from age_detection_service.core.model_service import ModelService


def get_model_service(request: Request) -> ModelService:
    """
    Dependencia de FastAPI para obtener el servicio de modelo cargado.

    Esta función se utiliza como proveedor de dependencias dentro de los
    endpoints de la API mediante `Depends`. Su propósito es recuperar la
    instancia del `ModelService` almacenada en el estado global de la
    aplicación (`app.state`).

    Antes de retornar el servicio, la función verifica que el modelo haya
    sido cargado correctamente. Si el modelo aún no está disponible, se
    lanza una excepción HTTP con código 503 indicando que el servicio
    todavía no está listo para procesar solicitudes.

    Args:
        request (Request):
            Objeto de solicitud HTTP proporcionado por FastAPI. Se utiliza
            para acceder al estado global de la aplicación mediante
            `request.app.state`.

    Returns:
        ModelService:
            Instancia del servicio encargado de ejecutar el modelo de
            detección de edad.

    Raises:
        HTTPException (503):
            Se lanza cuando el modelo aún no ha sido cargado o inicializado,
            indicando que el servicio de inferencia no está disponible.
    """
    service: ModelService = request.app.state.model_service
    if not service.is_loaded:
        raise HTTPException(503, detail="Modelo no disponible aún")
    return service
