from collections.abc import Iterator

from fastapi.testclient import TestClient

import apps.api_gateway.main as api_gateway_main
from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent


def test_websocket_accepts_connections(monkeypatch) -> None:

    def dummy_stream_local_detections(
        source: str | int, model_path: str, frame_step: int, max_frames: int | None
    ) -> Iterator[DetectionEvent]:

        assert source == "dummy.mp4"
        assert model_path == "dummy-model.pt"
        assert frame_step == 3
        assert max_frames == 7

        dummy_frame_detection_result = FrameDetectionResult(
            frame_index=1,
            detections=[],
            processing_time_ms=1.0,
        )

        event = DetectionEvent(
            source="dummy.mp4", detection_result=dummy_frame_detection_result
        )
        yield event

    monkeypatch.setattr(
        api_gateway_main, "stream_local_detections", dummy_stream_local_detections
    )

    client = TestClient(api_gateway_main.app)

    with client.websocket_connect(
        "/ws/detections?source=dummy.mp4&model_path=dummy-model.pt&frame_step=3&max_frames=7"
    ) as websocket:
        data = websocket.receive_json()
        assert data["event_type"] == "detection.frame.processed"
        assert "timestamp" in data
        assert "detection_result" in data
        assert data["detection_result"]["frame_index"] == 1
        assert data["detection_result"]["detections"] == []
        assert data["detection_result"]["processing_time_ms"] == 1.0
