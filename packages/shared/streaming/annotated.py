from collections.abc import Iterator

import cv2
from cv2.typing import MatLike

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

    if max_frames == 0:
        return iter(())

    video = LocalVideoCapture(source)
    detector = YoloDetector(model_path)

    success, first_frame = video.read_frame()

    if not success:
        video.release()
        raise ValueError("Could not read from video source")

    return _iter_annotated_frames(
        video=video,
        detector=detector,
        first_frame=first_frame,
        frame_step=frame_step,
        max_frames=max_frames,
        confidence_threshold=confidence_threshold,
    )


def _iter_annotated_frames(
    video: LocalVideoCapture,
    detector: YoloDetector,
    first_frame: MatLike,
    frame_step: int,
    max_frames: int | None,
    confidence_threshold: float,
) -> Iterator[bytes]:
    processed_frames = 0
    pending_frame: MatLike | None = first_frame

    try:
        while True:
            if max_frames is not None and processed_frames >= max_frames:
                break

            if pending_frame is None:
                success, frame = video.read_frame()

                if not success:
                    break
            else:
                frame = pending_frame
                pending_frame = None

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
