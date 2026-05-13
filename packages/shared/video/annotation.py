import cv2
from cv2.typing import MatLike

from packages.shared.detection.schemas import FrameDetectionResult


def draw_detections(
    frame: MatLike,
    detection_result: FrameDetectionResult,
) -> MatLike:
    annotated_frame = frame.copy()

    for detection in detection_result.detections:
        box = detection.bounding_box

        x1 = int(box.x1)
        y1 = int(box.y1)
        x2 = int(box.x2)
        y2 = int(box.y2)

        cv2.rectangle(annotated_frame, [x1, y1], [x2, y2], (0, 255, 0), 2)

        label = f"{detection.class_name} {detection.confidence:.2f}"

        x = x1
        y = max(y1 - 10, 0)

        cv2.putText(
            annotated_frame,
            label,
            [x, y],
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

    return annotated_frame
