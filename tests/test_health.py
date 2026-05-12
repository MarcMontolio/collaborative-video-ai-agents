from fastapi import status
from fastapi.testclient import TestClient

from apps.api_gateway.main import app


def test_health_check_endpoint_returns_ok() -> None:
    client = TestClient(app)
    
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "service": "api-gateway",
    }