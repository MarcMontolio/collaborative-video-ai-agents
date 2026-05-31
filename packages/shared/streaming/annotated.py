from collections.abc import Iterator

import cv2

from packages.shared.detection.yolo import YoloDetector
from packages.shared.video.annotation import draw_detections
from packages.shared.video.capture import LocalVideoCapture


def stream_annotated_frames(
    source: str | int,
    model_path: str,
    frame_step: int,
    max_frames: int | None,
    confidence_threshold: float = 0.5,
) -> Iterator[bytes]:
    if max_frames is not None and max_frames < 0:
        raise ValueError("--max-frames must be greater than or equal to 0")

    if frame_step < 1:
        raise ValueError("--frame-step must be greater than or equal to 1")

    if not 0 <= confidence_threshold <= 1:
        raise ValueError("--confidence-threshold must be between 0 and 1")

    video = LocalVideoCapture(source)

    try:
        detector = YoloDetector(model_path)
        processed_frames = 0

        while True:
            if max_frames is not None and processed_frames >= max_frames:
                break

            success, frame = video.read_frame()

            if not success:
                break

            processed_frames += 1

            if processed_frames % frame_step != 0:
                continue

            detection_result = detector.detect(
                frame,
                frame_index=processed_frames,
            )
            annotated_frame = draw_detections(
                frame,
                detection_result,
                confidence_threshold=confidence_threshold,
            )

            encoded_success, encoded_frame = cv2.imencode(".jpg", annotated_frame)

            if not encoded_success:
                continue

            yield encoded_frame.tobytes()

    finally:
        video.release()
