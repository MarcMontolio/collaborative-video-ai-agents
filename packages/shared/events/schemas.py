from datetime import UTC, datetime

from pydantic import BaseModel, Field

from packages.shared.detection.schemas import FrameDetectionResult


class DetectionEvent(BaseModel):
    event_type: str = Field(default="detection.frame.processed")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source: str | None = Field(default=None)
    detection_result: FrameDetectionResult