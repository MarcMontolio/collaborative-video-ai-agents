import pytest
from pydantic import ValidationError

from packages.shared.coordinator.detection import (
    DetectionSummary,
    summarise_detection_event,
)
from packages.shared.detection.schemas import (
    BoundingBox,
    DetectionResult,
    FrameDetectionResult,
)
from packages.shared.events.schemas import DetectionEvent


def test_detection_summary_accepts_valid_data() -> None:
    dummy_detection_summary = DetectionSummary(
        frame_index=1,
        source="dummy.mp4",
        total_detections=2,
        detected_classes=["person", "car"],
        highest_confidence=0.95,
    )

    assert dummy_detection_summary.frame_index == 1
    assert dummy_detection_summary.source == "dummy.mp4"
    assert dummy_detection_summary.total_detections == 2
    assert dummy_detection_summary.detected_classes == ["person", "car"]
    assert dummy_detection_summary.highest_confidence == 0.95


def test_detection_summary_rejects_confidence_greater_than_one() -> None:
    with pytest.raises(ValidationError):
        DetectionSummary(
            frame_index=1,
            source="dummy.mp4",
            total_detections=2,
            detected_classes=["person", "car"],
            highest_confidence=1.5,
        )


def test_summarise_detection_event_returns_detection_summary() -> None:
    dummy_detection_1 = DetectionResult(
        class_name="person",
        confidence=0.90,
        bounding_box=BoundingBox(x1=1, y1=2, x2=10, y2=20),
    )

    dummy_detection_2 = DetectionResult(
        class_name="car",
        confidence=0.70,
        bounding_box=BoundingBox(x1=5, y1=6, x2=30, y2=40),
    )

    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=1,
        detections=[dummy_detection_1, dummy_detection_2],
        processing_time_ms=12.5,
    )

    dummy_detection_event = DetectionEvent(
        source="dummy.mp4", detection_result=dummy_frame_detection_result
    )

    summary = summarise_detection_event(dummy_detection_event)

    assert isinstance(summary, DetectionSummary)
    assert summary.frame_index == 1
    assert summary.source == "dummy.mp4"
    assert summary.total_detections == 2
    assert summary.detected_classes == ["person", "car"]
    assert summary.highest_confidence == 0.90


def test_summarise_detection_event_handles_empty_detections() -> None:
    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=2, detections=[], processing_time_ms=5.0
    )

    dummy_detection_event = DetectionEvent(
        source="dummy.mp4",
        detection_result=dummy_frame_detection_result,
    )

    summary = summarise_detection_event(dummy_detection_event)

    assert summary.frame_index == 2
    assert summary.total_detections == 0
    assert summary.detected_classes == []
    assert summary.highest_confidence is None


def test_summarise_detection_event_deduplicates_detected_classes() -> None:
    dummy_detection_1 = DetectionResult(
        class_name="person",
        confidence=0.90,
        bounding_box=BoundingBox(x1=1, y1=2, x2=10, y2=20),
    )

    dummy_detection_2 = DetectionResult(
        class_name="person",
        confidence=0.70,
        bounding_box=BoundingBox(x1=5, y1=6, x2=30, y2=40),
    )

    dummy_detection_3 = DetectionResult(
        class_name="car",
        confidence=0.80,
        bounding_box=BoundingBox(x1=8, y1=9, x2=50, y2=60),
    )

    dummy_frame_detection_result = FrameDetectionResult(
        frame_index=3,
        detections=[dummy_detection_1, dummy_detection_2, dummy_detection_3],
        processing_time_ms=15.0,
    )

    dummy_detection_event = DetectionEvent(
        source="dummy.mp4",
        detection_result=dummy_frame_detection_result,
    )

    summary = summarise_detection_event(dummy_detection_event)

    assert summary.frame_index == 3
    assert summary.total_detections == 3
    assert summary.detected_classes == ["person", "car"]
    assert summary.highest_confidence == 0.90
