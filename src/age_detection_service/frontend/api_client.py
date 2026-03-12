import os

import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


def api_predict(image_bytes: bytes, filename: str) -> dict:
    """
    Envía una imagen al servicio de predicción de la API y retorna el resultado del análisis de edad.

    Esta función realiza una solicitud HTTP POST al endpoint `/predict` del servicio backend,
    enviando una imagen codificada en bytes como archivo multipart/form-data. El backend
    procesa la imagen mediante el modelo de detección de edad y devuelve un resultado
    estructurado en formato JSON.

    Args:
        image_bytes (bytes):
            Contenido binario de la imagen que se enviará al servicio de predicción.
            Normalmente corresponde a una imagen capturada por cámara o cargada
            desde la interfaz de la aplicación.

        filename (str):
            Nombre del archivo de imagen que se enviará en la solicitud HTTP.
            Este nombre se utiliza únicamente como identificador del archivo
            dentro de la solicitud multipart.

    Returns:
        dict:
            Diccionario con el resultado de la predicción retornado por la API.
            La estructura esperada del JSON puede incluir campos como:

            - `predicted_age_range` (str): rango de edad estimado por el modelo.
            - `confidence_percent` (float): porcentaje de confianza de la predicción.
            - `all_probabilities` (list[dict]): lista con probabilidades por rango de edad.

    Raises:
        httpx.HTTPStatusError:
            Se lanza si la respuesta del servidor contiene un código HTTP de error
            (por ejemplo, 4xx o 5xx).

        httpx.RequestError:
            Se lanza si ocurre un problema de conexión con el servidor, como
            fallos de red o timeout.
    """

    response = httpx.post(
        f"{API_BASE_URL}/predict",
        files={"image": (filename, image_bytes, "image/jpeg")},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()


def api_health() -> dict:
    """
    Consulta el estado de salud (health check) del servicio backend.

    Esta función envía una solicitud HTTP GET al endpoint `/health` de la API
    para verificar que el servicio se encuentra disponible y funcionando
    correctamente. Es útil para validar la conectividad entre el frontend
    y el backend antes de realizar solicitudes de predicción.

    Args:
        None.

    Returns:
        dict:
            Diccionario con la respuesta del endpoint de salud de la API.
            La estructura exacta depende de la implementación del backend,
            pero típicamente incluye campos como:

            - `status` (str): estado del servicio (por ejemplo `"ok"` o `"healthy"`).
            - `message` (str): descripción del estado del sistema.

    Raises:
        httpx.HTTPStatusError:
            Se lanza si la API responde con un código HTTP de error.

        httpx.RequestError:
            Se lanza si ocurre un problema de conexión con el servidor.
    """

    response = httpx.get(f"{API_BASE_URL}/health", timeout=10.0)
    response.raise_for_status()
    return response.json()
