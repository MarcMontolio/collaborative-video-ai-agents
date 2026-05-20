import argparse

from packages.shared.redis.client import get_redis_client
from packages.shared.redis.consumer import read_detection_stream_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Consume detection events from Redis Streams."
    )

    parser.add_argument(
        "--last-id",
        default="0",
        help="Redis Stream ID to start reading from. Defaults to 0.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Maximum number of messages to read. Defaults to 10.",
    )

    parser.add_argument(
        "--block-ms",
        type=int,
        default=None,
        help="Optional blocking timeout in milliseconds. Defaults to no blocking.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    client = get_redis_client()

    consumed_events = read_detection_stream_messages(
        client=client,
        last_id=args.last_id,
        count=args.count,
        block_ms=args.block_ms,
    )

    print(f"Consumed {len(consumed_events)} detection event(s) from Redis Streams.")

    for consumed_event in consumed_events:
        processing_time_ms = consumed_event.event.detection_result.processing_time_ms

        if processing_time_ms is None:
            processing_time = "unknown"
        else:
            processing_time = f"{processing_time_ms:.2f}"

        print(
            f"Message {consumed_event.message_id}",
            f"Frame {consumed_event.event.detection_result.frame_index}:",
            f"detections={len(consumed_event.event.detection_result.detections)}",
            f"processing_time_ms={processing_time}",
        )


if __name__ == "__main__":
    main()
