from redis import Redis

from packages.shared.alerts.schemas import (
    AlertEvent,
    create_alert_from_detection_summary,
)
from packages.shared.coordinator.detection import DetectionSummary
from packages.shared.redis.streams import ALERT_EVENT_STREAM


def publish_alert_event(client: Redis, alert: AlertEvent) -> str:
    message = {
        "event_type": alert.event_type,
        "payload": alert.model_dump_json(),
    }

    message_id = client.xadd(ALERT_EVENT_STREAM, message)

    return str(message_id)


def publish_alert_from_detection_summary(
    client: Redis,
    summary: DetectionSummary,
) -> str | None:
    alert = create_alert_from_detection_summary(summary)

    if alert is None:
        return None

    return publish_alert_event(client, alert)
