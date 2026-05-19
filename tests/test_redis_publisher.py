from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent
from packages.shared.redis.publisher import (
    publish_detection_event,
    publish_detection_events,
)
from packages.shared.redis.streams import DETECTION_EVENT_STREAM


def test_redis_publisher_with_mock_client() -> None:
    class DummyRedisClient:
        def __init__(self) -> None:
            self.stream_name = None
            self.message = None

        def xadd(self, stream_name, message) -> None:
            self.stream_name = stream_name
            self.message = message

            client_id = "1-0"

            return client_id

    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=1,
        detections=[],
        processing_time_ms=1.0,
    )

    dummy_detection_event = DetectionEvent(
        detection_result=dummy_frame_detection_result
    )

    dummy_client = DummyRedisClient()

    message_id = publish_detection_event(dummy_client, dummy_detection_event)

    assert message_id == "1-0"
    assert dummy_client.stream_name == DETECTION_EVENT_STREAM
    assert dummy_client.message is not None
    assert dummy_client.message["event_type"] == "detection.frame.processed"
    assert "detection_result" in dummy_client.message["payload"]
    assert '"frame_index":1' in dummy_client.message["payload"]
    assert isinstance(dummy_client.message["payload"], str)


def test_publish_detection_events_returns_published_count() -> None:
    class DummyRedisClient:
        def __init__(self) -> None:
            self.calls = []

        def xadd(self, stream_name, message):
            self.calls.append(
                {
                    "stream_name": stream_name,
                    "message": message,
                }
            )

            return f"{len(self.calls)}-0"

    dummy_frame_detection_result_1 = FrameDetectionResult(
        frame_index=1,
        detections=[],
        processing_time_ms=1.0,
    )

    dummy_frame_detection_result_2 = FrameDetectionResult(
        frame_index=2,
        detections=[],
        processing_time_ms=1.0,
    )

    dummy_detection_event_1 = DetectionEvent(
        detection_result=dummy_frame_detection_result_1
    )

    dummy_detection_event_2 = DetectionEvent(
        detection_result=dummy_frame_detection_result_2
    )

    dummy_client = DummyRedisClient()

    published_count = publish_detection_events(
        dummy_client, [dummy_detection_event_1, dummy_detection_event_2]
    )

    assert published_count == 2
    assert len(dummy_client.calls) == 2
    assert dummy_client.calls[0]["stream_name"] == DETECTION_EVENT_STREAM
    assert dummy_client.calls[1]["stream_name"] == DETECTION_EVENT_STREAM
    assert '"frame_index":1' in dummy_client.calls[0]["message"]["payload"]
    assert '"frame_index":2' in dummy_client.calls[1]["message"]["payload"]
