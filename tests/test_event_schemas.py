from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent


def test_detection_event_accepts_valid_data() -> None:
    data_frame_detection_result = FrameDetectionResult(
        frame_index=0,
        detections=[],
        processing_time_ms=12.5
    )
    
    event = DetectionEvent(
        detection_result=data_frame_detection_result
    )
    
    assert event.event_type == "detection.frame.processed"
    assert event.source is None
    assert event.timestamp is not None
    assert event.detection_result == data_frame_detection_result
    
    
def test_detection_event_can_be_serialized_to_json() -> None:
    data_frame_detection_result = FrameDetectionResult(
        frame_index=0,
        detections=[],
        processing_time_ms=12.5
    )
    
    detection_event = DetectionEvent(
        detection_result=data_frame_detection_result
    )
    
    detection_event_json = detection_event.model_dump_json()
    
    assert isinstance(detection_event_json, str)
    assert "detection.frame.processed" in detection_event_json
    assert "detection_result" in detection_event_json
    
    