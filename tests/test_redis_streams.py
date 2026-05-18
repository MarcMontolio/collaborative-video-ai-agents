from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent
from packages.shared.redis.schemas import (
    DetectionStreamPayload,
    detection_event_to_stream_payload,
)
from packages.shared.redis.streams import ALERT_EVENT_STREAM, DETECTION_EVENT_STREAM


def test_redis_streams() -> None:
    assert DETECTION_EVENT_STREAM == "detection-events"
    assert ALERT_EVENT_STREAM == "alert-events"
    

def test_redis_payload_schemas() -> None:
    dummy_detection_stream_payload = DetectionStreamPayload(
        event_type="detection.frame.processed",
        payload='{"frame_index": 1}'
    )
    
    assert dummy_detection_stream_payload.event_type == "detection.frame.processed"
    assert dummy_detection_stream_payload.payload == '{"frame_index": 1}'
    

def test_detection_event_to_stream_payload() -> None:
    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=1,
        detections=[],
        processing_time_ms=1.0
    )
    
    dummy_detection_event = DetectionEvent(
        detection_result=dummy_frame_detection_result
    )
    
    dummy_event = detection_event_to_stream_payload(dummy_detection_event)
    
    assert dummy_event.event_type == "detection.frame.processed"
    assert isinstance(dummy_event.payload, str)
    assert '"detection_result"' in dummy_event.payload
    assert '"frame_index":1' in dummy_event.payload
    
    