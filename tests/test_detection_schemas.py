import pytest
from pydantic import ValidationError

from packages.shared.detection.schemas import (
    BoundingBox,
    DetectionResult,
    FrameDetectionResult,
)


def test_bounding_box_accepts_valid_coordinates() -> None:
    data = {
        "x1": 1,
        "y1": 3,
        "x2": 6,
        "y2": 7,
    }

    box = BoundingBox(**data)

    assert box.x1 == 1
    assert box.y1 == 3
    assert box.x2 == 6
    assert box.y2 == 7


def test_detection_result_accepts_valid_detection() -> None:
    data_box = {
        "x1": 1,
        "y1": 3,
        "x2": 6,
        "y2": 7,
    }

    box = BoundingBox(**data_box)

    data_detection = {
        "class_name": "cat",
        "confidence": 0.35,
        "bounding_box": box,
    }

    detection_result = DetectionResult(**data_detection)

    assert detection_result.class_name == "cat"
    assert detection_result.confidence == 0.35
    assert detection_result.bounding_box == box


def test_detection_result_refuses_confidence_greater_than_one() -> None:
    data_box = {
        "x1": 1,
        "y1": 3,
        "x2": 6,
        "y2": 7,
    }

    box = BoundingBox(**data_box)

    data_detection = {
        "class_name": "cat",
        "confidence": 1.35,
        "bounding_box": box,
    }

    with pytest.raises(ValidationError):
        DetectionResult(**data_detection)


def test_frame_detection_result_accepts_empty_list() -> None:
    data_frame_detection = {
        "frame_index": 0,
        "detections": [],
        "processing_time_ms": 3,
    }

    frame_detection_result = FrameDetectionResult(**data_frame_detection)

    assert frame_detection_result.frame_index == 0
    assert frame_detection_result.detections == []
    assert frame_detection_result.processing_time_ms == 3
