from datetime import UTC, datetime

from pydantic import BaseModel, Field

from packages.shared.coordinator.detection import DetectionSummary


class AlertEvent(BaseModel):
    event_type: str = "alert.detection.generated"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    severity: str = "info"
    message: str
    source: str | None = None
    frame_index: int | None = Field(default=None, ge=0)
    detected_classes: list[str] = Field(default_factory=list)


def create_alert_from_detection_summary(summary: DetectionSummary) -> AlertEvent | None:
    if summary.total_detections == 0:
        return None
    return AlertEvent(
        severity="info",
        message=f"Detected {summary.total_detections} object(s)",
        source=summary.source,
        frame_index=summary.frame_index,
        detected_classes=summary.detected_classes,
    )
