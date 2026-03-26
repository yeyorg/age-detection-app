"""
Punto de entrada mantenido por compatibilidad con versiones anteriores.

Este módulo permite que scripts que usan `age_detection_service.API.main`
sigan funcionando, delegando la ejecución al nuevo módulo `age_detection_service.api.app`.
"""

from age_detection_service.api.app import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
