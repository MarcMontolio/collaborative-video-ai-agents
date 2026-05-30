import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from packages.shared.alerts.schemas import create_alert_from_detection_summary
from packages.shared.config import get_settings
from packages.shared.coordinator.detection import summarise_detection_event
from packages.shared.streaming.local import stream_local_detections


def get_next_stream_event(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "api-gateway",
        }

    @app.websocket("/ws/detections")
    async def detection_websocket(
        websocket: WebSocket,
        source: str = "0",
        model_path: str = "yolo11n.pt",
        frame_step: int = 5,
        max_frames: int | None = None,
    ) -> None:
        await websocket.accept()

        video_source = int(source) if source.isdigit() else source

        iterator = stream_local_detections(
            source=video_source,
            model_path=model_path,
            frame_step=frame_step,
            max_frames=max_frames,
        )

        try:
            while True:
                event = await asyncio.to_thread(get_next_stream_event, iterator)

                if event is None:
                    break

                await websocket.send_json(event.model_dump(mode="json"))

            await websocket.close()
        except WebSocketDisconnect:
            pass

    @app.websocket("/ws/dashboard")
    async def dashboard_websocket(
        websocket: WebSocket,
        source: str = "0",
        model_path: str = "yolo11n.pt",
        frame_step: int = 5,
        max_frames: int | None = None,
    ) -> None:
        await websocket.accept()

        video_source = int(source) if source.isdigit() else source
        iterator = stream_local_detections(
            source=video_source,
            model_path=model_path,
            frame_step=frame_step,
            max_frames=max_frames,
        )

        try:
            while True:
                event = await asyncio.to_thread(get_next_stream_event, iterator)

                if event is None:
                    break

                await websocket.send_json(
                    {
                        "type": "detection",
                        "payload": event.model_dump(mode="json"),
                    }
                )

                summary = summarise_detection_event(event)
                alert = create_alert_from_detection_summary(summary)

                if alert is None:
                    continue

                await websocket.send_json(
                    {"type": "alert", "payload": alert.model_dump(mode="json")}
                )

            await websocket.close()
        except WebSocketDisconnect:
            pass

    return app


app = create_app()
