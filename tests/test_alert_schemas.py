import pytest
from pydantic import ValidationError

from packages.shared.alerts.schemas import (
    AlertEvent,
    create_alert_from_detection_summary,
)
from packages.shared.coordinator.detection import DetectionSummary


def test_alert_event_accepts_valid_data() -> None:
    dummy_alert_event = AlertEvent(
        message="Person detected",
        source="dummy.mp4",
        frame_index=1,
        detected_classes=["person"],
    )

    assert dummy_alert_event.event_type == "alert.detection.generated"
    assert dummy_alert_event.severity == "info"
    assert dummy_alert_event.message == "Person detected"
    assert dummy_alert_event.source == "dummy.mp4"
    assert dummy_alert_event.frame_index == 1
    assert dummy_alert_event.detected_classes == ["person"]
    assert dummy_alert_event.timestamp is not None


def test_alert_event_rejects_negative_frame_index() -> None:
    with pytest.raises(ValidationError):
        AlertEvent(
            message="Invalid frame",
            frame_index=-1,
        )


def test_create_alert_from_detection_summary_returns_alert_event() -> None:
    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=2,
        detected_classes=["person", "car"],
        highest_confidence=0.95,
    )

    alert = create_alert_from_detection_summary(summary)

    assert isinstance(alert, AlertEvent)
    assert alert.event_type == "alert.detection.generated"
    assert alert.severity == "info"
    assert alert.message == "Person detected in frame 1"
    assert alert.source == "dummy.mp4"
    assert alert.frame_index == 1
    assert alert.detected_classes == ["person", "car"]


def test_create_alert_from_detection_summary_returns_none_without_detections() -> None:
    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=0,
        detected_classes=[],
        highest_confidence=None,
    )

    alert = create_alert_from_detection_summary(summary)

    assert alert is None


def test_create_alert_from_detection_summary_returns_none_without_person() -> None:
    summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=2,
        detected_classes=["car", "kite"],
        highest_confidence=0.95
    )
    
    alert = create_alert_from_detection_summary(summary)
    
    assert alert is None