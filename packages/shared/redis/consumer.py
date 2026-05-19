from packages.shared.events.schemas import DetectionEvent
from packages.shared.redis.streams import DETECTION_EVENT_STREAM
from redis import Redis


def parse_detection_stream_message(message: dict) -> DetectionEvent:
    payload = message["payload"]
    event = DetectionEvent.model_validate_json(payload)
    return event


def read_detection_stream_messages(
    client: Redis,
    last_id: str = "0",
    count: int = 10,
    block_ms: int | None = None,
) -> list[DetectionEvent]:
    events_list = []

    stream_entries = client.xread(
        streams={DETECTION_EVENT_STREAM: last_id},
        count=count,
        block=block_ms,
    )

    for _stream_name, messages in stream_entries:
        for _message_id, message in messages:
            parsed_event = parse_detection_stream_message(message)
            events_list.append(parsed_event)

    return events_list
