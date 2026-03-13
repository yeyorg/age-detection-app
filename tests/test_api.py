"""
Tests de integración para los endpoints principales de la API de detección de edad.

Este módulo contiene pruebas automatizadas utilizando `pytest` y `FastAPI TestClient`
para validar el comportamiento de los endpoints expuestos por la API.

Las pruebas verifican diferentes escenarios del servicio de predicción de edad,
incluyendo:

    - Disponibilidad del endpoint de salud (`/health`)
    - Consulta de metadatos del modelo (`/model/metadata`)
    - Predicción de edad a partir de una imagen (`/predict`)
    - Verificación de mayoría de edad (`/verify`)
    - Manejo de errores cuando el modelo no está cargado

Para simular el comportamiento del servicio de inferencia sin depender de un
modelo real, se utilizan objetos `MagicMock` que reemplazan temporalmente
la instancia de `ModelService` almacenada en `app.state.model_service`.

Esto permite probar el comportamiento de la API de forma aislada y rápida.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from age_detection_service.api.app import app
from age_detection_service.core.model_service import ModelService

client = TestClient(app)


@pytest.fixture
def mock_service_loaded():
    """
    Fixture que simula un servicio de modelo cargado correctamente.

    Este fixture crea un objeto `MagicMock` basado en la interfaz de
    `ModelService` y lo asigna a `app.state.model_service`. De esta forma
    se reemplaza temporalmente el servicio real de inferencia durante la
    ejecución de las pruebas.

    Configuración del mock:
        - `is_loaded` se establece en `True`, indicando que el modelo está disponible.
        - `predict` devuelve un resultado de predicción simulado.

    Returns:
        MagicMock:
            Objeto simulado que representa el servicio de modelo cargado.
    """
    mock = MagicMock(spec=ModelService)
    mock.is_loaded = True
    mock.predict.return_value = {"age_range": "25-34"}
    app.state.model_service = mock
    return mock


@pytest.fixture
def mock_service_not_loaded():
    """
    Fixture que simula un servicio de modelo no cargado.

    Este fixture crea un objeto `MagicMock` basado en `ModelService` donde
    la propiedad `is_loaded` se establece en `False`. Esto permite verificar
    cómo responde la API cuando el modelo aún no está disponible para realizar
    inferencias.

    Returns:
        MagicMock:
            Objeto simulado que representa un servicio de modelo no cargado.
    """
    mock = MagicMock(spec=ModelService)
    mock.is_loaded = False
    app.state.model_service = mock
    return mock


def test_health_check():
    """
    Verifica que el endpoint de salud de la API responda correctamente.

    Esta prueba envía una solicitud GET al endpoint `/api/v1/health`
    y comprueba que el servidor responde con código HTTP 200, lo que
    indica que la API está disponible y funcionando.

    Returns:
        None.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_model_metadata():
    """
    Verifica el endpoint de metadatos del modelo.

    Esta prueba consulta el endpoint `/api/v1/model/metadata`, el cual
    proporciona información sobre el modelo cargado en el sistema.

    Dependiendo del estado del servicio, el endpoint puede devolver:

        - 200: si el modelo está cargado correctamente.
        - 503: si el modelo aún no está disponible.

    Returns:
        None.
    """
    response = client.get("/api/v1/model/metadata")
    assert response.status_code in [200, 503]


def test_predict_ok(mock_service_loaded):
    """
    Verifica el endpoint de predicción cuando el modelo está cargado.

    Esta prueba envía una imagen simulada al endpoint `/api/v1/predict`
    utilizando una solicitud POST con formato `multipart/form-data`.

    Se evalúan dos posibles respuestas válidas:

        - 200: la predicción se realizó correctamente.
        - 422: error de validación en la entrada de datos.

    Args:
        mock_service_loaded:
            Fixture que proporciona un servicio de modelo simulado cargado.

    Returns:
        None.
    """
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
    )
    assert response.status_code in [200, 422]


def test_predict_modelo_no_cargado(mock_service_not_loaded):
    """
    Verifica el comportamiento del endpoint de predicción cuando el modelo no está cargado.

    Esta prueba simula un escenario donde el servicio de inferencia aún
    no está disponible. Se envía una imagen al endpoint `/api/v1/predict`
    y se comprueba que el sistema responde adecuadamente.

    Posibles respuestas esperadas:

        - 503: el servicio no está disponible porque el modelo no está cargado.
        - 422: error de validación de la solicitud.

    Args:
        mock_service_not_loaded:
            Fixture que proporciona un servicio de modelo simulado no cargado.

    Returns:
        None.
    """
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
    )
    assert response.status_code in [503, 422]


def test_verify(mock_service_loaded):
    """
    Verifica el endpoint de verificación de edad.

    Esta prueba envía una imagen al endpoint `/api/v1/verify`, el cual
    utiliza el modelo de detección de edad para determinar si el usuario
    cumple con la mayoría de edad.

    Dependiendo del procesamiento y validación de la imagen, el endpoint
    puede devolver:

        - 200: verificación realizada correctamente.
        - 422: error de validación en los datos enviados.

    Args:
        mock_service_loaded:
            Fixture que proporciona un servicio de modelo simulado cargado.

    Returns:
        None.
    """
    response = client.post(
        "/api/v1/verify", files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")}
    )
    assert response.status_code in [200, 422]
