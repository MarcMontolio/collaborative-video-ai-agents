import numpy as np
import pytest

import packages.shared.streaming.local as local_streaming
from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent
from packages.shared.streaming.local import stream_local_detections


def test_stream_local_detections_rejects_frame_step_is_zero_or_less() -> None:
    with pytest.raises(ValueError):
        list(
            stream_local_detections(
                source="samples/test-video.mp4",
                model_path="yolo11n.pt",
                frame_step=0,
                max_frames=None,
            )
        )


def test_stream_local_detections_rejects_negative_max_frames() -> None:
    with pytest.raises(ValueError):
        list(
            stream_local_detections(
                source="samples/test-video.mp4",
                model_path="yolo11n.pt",
                frame_step=1,
                max_frames=-1,
            )
        )


def test_stream_local_detections_yields_detection_events(monkeypatch) -> None:
    class DummyYoloDetector:
        def __init__(self, model_path):

            self.model_path = model_path

        def detect(self, frame, frame_index):
            return FrameDetectionResult(
                frame_index=frame_index,
                detections=[],
                processing_time_ms=1.0,
            )

    class DummyVideoCapture:
        def __init__(self, source):

            self.source = source
            self.read_count = 0

        def read_frame(self):
            if self.read_count == 0:
                self.read_count += 1
                dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
                return True, dummy_frame
            return False, None

        def release(self):
            pass

    monkeypatch.setattr(local_streaming, "LocalVideoCapture", DummyVideoCapture)
    monkeypatch.setattr(local_streaming, "YoloDetector", DummyYoloDetector)

    events = list(
        stream_local_detections(
            source="dummy.mp4",
            model_path="dummy-model.pt",
            frame_step=1,
            max_frames=1,
        )
    )

    assert len(events) == 1
    assert isinstance(events[0], DetectionEvent)
    assert events[0].source == "dummy.mp4"
    assert events[0].detection_result.frame_index == 1
    assert events[0].detection_result.processing_time_ms == 1.0
