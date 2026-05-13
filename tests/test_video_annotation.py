import numpy as np

from packages.shared.detection.schemas import (
    BoundingBox,
    DetectionResult,
    FrameDetectionResult,
)
from packages.shared.video.annotation import draw_detections


def test_draw_detections_returns_frame_with_same_shape() -> None:
    dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)

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

    frame_detection_result = FrameDetectionResult(
        frame_index=0,
        detections=[detection_result],
    )

    annotated_frame = draw_detections(dummy_frame, frame_detection_result)

    assert annotated_frame.shape == dummy_frame.shape
    assert np.any(annotated_frame != dummy_frame)
