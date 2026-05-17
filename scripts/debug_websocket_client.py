import argparse
import asyncio

import websockets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Debug client for detection WebSocket events."
    )
    
    parser.add_argument(
        "--url",
        default="ws://127.0.0.1:8000/ws/detections",
        help="WebSocket URL"
    )
    
    return parser.parse_args()


async def run_client(url: str) -> None:
    async with websockets.connect(url) as websocket:
        print(f"Connecting to {url}")
        print("Waiting for events")
        async for message in websocket:
            print(f"Received: {message}")


def main() -> None:
    try:
        args = parse_args()
        asyncio.run(run_client(args.url))
    except OSError:
        print("Cannot connect to the server. Please check if the API is running.")
    
    
if __name__ == "__main__":
    main()