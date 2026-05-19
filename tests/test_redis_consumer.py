from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent
from packages.shared.redis.consumer import (
    parse_detection_stream_message,
    read_detection_stream_messages,
)
from packages.shared.redis.streams import DETECTION_EVENT_STREAM


def test_parse_detection_stream_message_returns_detection_event() -> None:
    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=1,
        detections=[],
        processing_time_ms=1.0,
    )

    dummy_detection_event = DetectionEvent(
        detection_result=dummy_frame_detection_result
    )

    dummy_redis_message = {
        "event_type": dummy_detection_event.event_type,
        "payload": dummy_detection_event.model_dump_json(),
    }

    parsed_event = parse_detection_stream_message(dummy_redis_message)

    assert isinstance(parsed_event, DetectionEvent)
    assert parsed_event.event_type == "detection.frame.processed"
    assert parsed_event.detection_result.frame_index == 1


def test_read_detection_stream_messages_returns_detection_events() -> None:
    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=1,
        detections=[],
        processing_time_ms=1.0,
    )

    dummy_detection_event = DetectionEvent(
        detection_result=dummy_frame_detection_result,
    )

    class DummyRedisClient:
        def __init__(self) -> None:
            self.streams = None
            self.count = None
            self.block = None

        def xread(self, streams, count, block):
            self.streams = streams
            self.count = count
            self.block = block

            return [
                (
                    DETECTION_EVENT_STREAM,
                    [
                        (
                            "1-0",
                            {
                                "event_type": dummy_detection_event.event_type,
                                "payload": dummy_detection_event.model_dump_json(),
                            },
                        )
                    ],
                )
            ]

    dummy_client = DummyRedisClient()

    events = read_detection_stream_messages(dummy_client)

    assert dummy_client.streams == {DETECTION_EVENT_STREAM: "0"}
    assert dummy_client.count == 10
    assert dummy_client.block is None

    assert len(events) == 1
    assert isinstance(events[0], DetectionEvent)
    assert events[0].event_type == "detection.frame.processed"
    assert events[0].detection_result.frame_index == 1
