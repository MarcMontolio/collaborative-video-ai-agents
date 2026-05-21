from pydantic import BaseModel, Field

from packages.shared.events.schemas import DetectionEvent


class DetectionSummary(BaseModel):
    frame_index: int = Field(ge=0)
    source: str | None = None
    total_detections: int = Field(ge=0)
    detected_classes: list[str]
    highest_confidence: float | None = Field(default=None, ge=0, le=1)


def summarise_detection_event(event: DetectionEvent) -> DetectionSummary:
    detection_result = event.detection_result
    detections = detection_result.detections

    detected_classes = list(
        dict.fromkeys(detection.class_name for detection in detections)
    )

    if not detections:
        highest_confidence = None
    else:
        highest_confidence = max(detection.confidence for detection in detections)

    return DetectionSummary(
        frame_index=detection_result.frame_index,
        source=event.source,
        total_detections=len(detections),
        detected_classes=detected_classes,
        highest_confidence=highest_confidence,
    )
