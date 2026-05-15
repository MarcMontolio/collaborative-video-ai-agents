from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from packages.shared.config import get_settings
from packages.shared.detection.schemas import FrameDetectionResult
from packages.shared.events.schemas import DetectionEvent


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
    async def detection_websocket(websocket: WebSocket) -> None:
        await websocket.accept()
        frame_detection_result_dummy = FrameDetectionResult(
            frame_index=0,
            detections=[],
            processing_time_ms=0.0,
        )

        detection_event_dummy = DetectionEvent(
            detection_result=frame_detection_result_dummy
        ).model_dump(mode="json")

        try:
            await websocket.send_json(detection_event_dummy)
            await websocket.close()
        except WebSocketDisconnect:
            pass

    return app


app = create_app()
