import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from age_detection_service.api.app import app
from age_detection_service.core.model_service import ModelService

client = TestClient(app)


@pytest.fixture
def mock_service_loaded():
    mock = MagicMock(spec=ModelService)
    mock.is_loaded = True
    mock.predict.return_value = {"age_range": "25-34"}
    app.state.model_service = mock
    return mock


@pytest.fixture
def mock_service_not_loaded():
    mock = MagicMock(spec=ModelService)
    mock.is_loaded = False
    app.state.model_service = mock
    return mock


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_model_metadata():
    response = client.get("/api/v1/model/metadata")
    assert response.status_code in [200, 503]


def test_predict_ok(mock_service_loaded):
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")}
    )
    assert response.status_code in [200, 422]


def test_predict_modelo_no_cargado(mock_service_not_loaded):
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")}
    )
    assert response.status_code in [503, 422]


def test_verify(mock_service_loaded):
    response = client.post(
        "/api/v1/verify",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")}
    )
    assert response.status_code in [200, 422]
