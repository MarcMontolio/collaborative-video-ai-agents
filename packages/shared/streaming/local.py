from collections.abc import Iterator

from packages.shared.detection.yolo import YoloDetector
from packages.shared.events.schemas import DetectionEvent
from packages.shared.video.capture import LocalVideoCapture


def stream_local_detections(
    source: str | int,
    model_path: str,
    frame_step: int,
    max_frames: int | None,
) -> Iterator[DetectionEvent]:

    if max_frames is not None and max_frames < 0:
        raise ValueError("--max-frames must be greater than or equal to 0")

    if frame_step < 1:
        raise ValueError("--frame-step must be greater than or equal to 1")

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

            detection_result = detector.detect(frame, frame_index=processed_frames)
            event = DetectionEvent(
                detection_result=detection_result, source=str(source)
            )
            yield event

    finally:
        video.release()
