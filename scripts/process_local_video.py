import argparse

from packages.shared.detection.yolo import YoloDetector
from packages.shared.video.capture import LocalVideoCapture


def parse_video_source(source: str) -> str | int:
    if source.isdigit():
        return int(source)

    return source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a local video source frame by frame."
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Video source path or webcam index.",
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Maximum number of frames to process.",
    )

    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="YOLO model path or model name.",
    )

    parser.add_argument(
        "--frame-step",
        type=int,
        default=1,
        help="Run detection every N frames.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.max_frames is not None and args.max_frames < 0:
        raise ValueError("--max-frames must be greater than or equal to 0")

    if args.frame_step < 1:
        raise ValueError("--frame-step must be greater than or equal to 1")

    source = parse_video_source(args.source)

    video = LocalVideoCapture(source)
    detector = YoloDetector(model_path=args.model)

    try:
        print(f"Video metadata: {video.metadata}")

        processed_frames = 0
        detection_frames = 0

        while True:
            if args.max_frames is not None and processed_frames >= args.max_frames:
                break

            success, frame = video.read_frame()

            if not success:
                break

            processed_frames += 1

            if processed_frames % args.frame_step != 0:
                continue

            detection_result = detector.detect(frame, frame_index=processed_frames)
            detection_frames += 1

            print(
                f"Processed frame {processed_frames}: "
                f"detections={len(detection_result.detections)} "
                f"processing_time_ms={detection_result.processing_time_ms:.2f}"
            )

            for detection in detection_result.detections:
                print(
                    f"  - {detection.class_name} "
                    f"confidence={detection.confidence:.2f}"
                )

        print(f"Processed {processed_frames} frame(s).")
        print(f"Ran detection on {detection_frames} frame(s).")
    finally:
        video.release()


if __name__ == "__main__":
    main()