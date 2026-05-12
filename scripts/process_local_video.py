import argparse

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
        help="Video source path or webcam index."
    )
    
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Maximun number of frames to process."
    )
    
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.max_frames is not None and args.max_frames < 0:
        raise ValueError("--max-frames must be greater than or equal to 0")

    source = parse_video_source(args.source)

    video = LocalVideoCapture(source)

    try:
        print(f"Video metadata: {video.metadata}")

        processed_frames = 0

        while True:
            if args.max_frames is not None and processed_frames >= args.max_frames:
                break

            success, frame = video.read_frame()

            if not success:
                break

            processed_frames += 1
            frame_shape = frame.shape if frame is not None else None

            print(f"Processed frame {processed_frames}: shape={frame_shape}")

        print(f"Processed {processed_frames} frame(s).")
    finally:
        video.release()
        
        
if __name__ == "__main__":
    main()