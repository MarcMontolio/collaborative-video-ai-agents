from fastapi.testclient import TestClient

from apps.api_gateway.main import app


def test_websocket_accepts_connections() -> None:
    client = TestClient(app)
    
    with client.websocket_connect("/ws/detections") as websocket:
        data = websocket.receive_json()
        assert data["event_type"] == "detection.frame.processed"
        assert "timestamp" in data
        assert "detection_result" in data
        assert data["detection_result"]["frame_index"] == 0
        assert data["detection_result"]["detections"] == []
        assert data ["detection_result"]["processing_time_ms"] == 0.0
        