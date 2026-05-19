from collections.abc import Iterable

from packages.shared.events.schemas import DetectionEvent
from packages.shared.redis.schemas import detection_event_to_stream_payload
from packages.shared.redis.streams import DETECTION_EVENT_STREAM
from redis import Redis


def publish_detection_event(client: Redis, event: DetectionEvent) -> str:
    payload = detection_event_to_stream_payload(event)
    message = {
        "event_type": payload.event_type,
        "payload": payload.payload,
    }
    message_id = client.xadd(DETECTION_EVENT_STREAM, message)
    return str(message_id)


def publish_detection_events(
    client: Redis,
    events: Iterable[DetectionEvent],
) -> int:
    published_count = 0

    for event in events:
        publish_detection_event(client, event)
        published_count += 1
    return published_count
