import os

import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


def api_predict(image_bytes: bytes, filename: str) -> dict:
    """Envía una imagen a la API y retorna la predicción de edad."""
    response = httpx.post(
        f"{API_BASE_URL}/predict",
        files={"image": (filename, image_bytes, "image/jpeg")},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()


def api_health() -> dict:
    """Consulta el estado de salud de la API."""
    response = httpx.get(f"{API_BASE_URL}/health", timeout=10.0)
    response.raise_for_status()
    return response.json()
