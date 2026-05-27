from packages.shared.alerts.publisher import (
    publish_alert_event,
    publish_alert_from_detection_summary,
)
from packages.shared.alerts.schemas import AlertEvent
from packages.shared.coordinator.detection import DetectionSummary
from packages.shared.redis.streams import ALERT_EVENT_STREAM


def test_publish_alert_event_with_mock_client() -> None:
    class DummyRedisClient:
        def __init__(self):
            self.stream_name = None
            self.message = None

        def xadd(self, stream_name, message) -> None:
            self.stream_name = stream_name
            self.message = message

            client_id = "1-0"

            return client_id

    dummy_alert_event = AlertEvent(
        message="Detected 2 object(s)",
        source="dummy.mp4",
        frame_index=1,
        detected_classes=["person", "car"],
    )

    dummy_client = DummyRedisClient()

    message_id = publish_alert_event(dummy_client, dummy_alert_event)

    assert message_id == "1-0"
    assert dummy_client.stream_name == ALERT_EVENT_STREAM
    assert dummy_client.message is not None
    assert dummy_client.message["event_type"] == "alert.detection.generated"
    assert isinstance(dummy_client.message["payload"], str)
    assert "Detected 2 object(s)" in dummy_client.message["payload"]
    assert '"frame_index":1' in dummy_client.message["payload"]


def test_publish_alert_from_detection_summary_publishes_generated_alert() -> None:
    class DummyRedisClient:
        def __init__(self) -> None:
            self.stream_name = None
            self.message = None

        def xadd(self, stream_name, message) -> str:
            self.stream_name = stream_name
            self.message = message
            return "1-0"

    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=2,
        detected_classes=["person", "car"],
        highest_confidence=0.95,
    )

    dummy_client = DummyRedisClient()

    message_id = publish_alert_from_detection_summary(dummy_client, summary)

    assert message_id == "1-0"
    assert dummy_client.stream_name == ALERT_EVENT_STREAM
    assert dummy_client.message is not None
    assert dummy_client.message["event_type"] == "alert.detection.generated"
    assert "Person detected in frame 1" in dummy_client.message["payload"]


def test_publish_alert_from_detection_summary_skips_empty_summary() -> None:
    class DummyRedisClient:
        def __init__(self) -> None:
            self.was_called = False

        def xadd(self, stream_name, message) -> str:
            self.was_called = True
            return "1-0"

    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=0,
        detected_classes=[],
        highest_confidence=None,
    )

    dummy_client = DummyRedisClient()

    message_id = publish_alert_from_detection_summary(dummy_client, summary)

    assert message_id is None
    assert dummy_client.was_called is False


def test_publish_alert_from_detection_summary_skips_summary_without_person() -> None:
    class DummyRedisClient:
        def __init__(self) -> None:
            self.was_called = False
            
        def xadd(self, stream_name, message) -> str:
            self.was_called = True
            return "1-0"
        
    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=2,
        detected_classes=["car", "kite"],
        highest_confidence=0.95,
    )
    
    dummy_client = DummyRedisClient()
    
    message_id = publish_alert_from_detection_summary(dummy_client, summary)
    
    assert message_id is None
    assert dummy_client.was_called is False