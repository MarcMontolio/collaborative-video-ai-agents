import pytest
from scripts.process_local_video import parse_video_source

from packages.shared.video.capture import LocalVideoCapture


def test_import_parse_video_source_converts_webcam_index_to_int() -> None:
    result = parse_video_source("0")

    assert result == 0


def test_import_parse_video_source_keeps_file_path_as_string() -> None:
    result = parse_video_source("samples/test-video.mp4")

    assert result == "samples/test-video.mp4"


def test_local_video_capture_fails_on_invalid_source() -> None:
    dummy_path = "samples/this-file-does-not-exist.mp4"

    with pytest.raises(ValueError):
        LocalVideoCapture(dummy_path)
