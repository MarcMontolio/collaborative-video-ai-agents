import argparse

from packages.shared.redis.client import get_redis_client
from packages.shared.redis.publisher import publish_detection_events
from packages.shared.streaming.local import stream_local_detections


def parse_video_source(source: str) -> str | int:
    if source.isdigit():
        return int(source)

    return source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish local detection events to Redis Streams."
    )

    parser.add_argument(
        "--source",
        default="0",
        help="Video source path or webcam index. Defaults to 0.",
    )

    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="YOLO model path or model name.",
    )

    parser.add_argument(
        "--frame-step",
        type=int,
        default=5,
        help="Run detection every N frames.",
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Maximum number of frames to process.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.frame_step < 1:
        raise ValueError("frame_step must be greater than or equal to 1")

    if args.max_frames is not None and args.max_frames < 0:
        raise ValueError("max_frames must be greater than or equal to 0")

    source = parse_video_source(args.source)

    client = get_redis_client()

    events = stream_local_detections(
        source=source,
        model_path=args.model,
        frame_step=args.frame_step,
        max_frames=args.max_frames,
    )
    published_count = publish_detection_events(client, events)

    print(f"Published {published_count} detection event(s) to Redis Streams.")


if __name__ == "__main__":
    main()
