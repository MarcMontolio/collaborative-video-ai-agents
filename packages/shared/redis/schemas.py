from pydantic import BaseModel

from packages.shared.events.schemas import DetectionEvent


class DetectionStreamPayload(BaseModel):
    event_type: str
    payload: str
    
    
def detection_event_to_stream_payload(
    event: DetectionEvent,
) -> DetectionStreamPayload:
    return DetectionStreamPayload(
        event_type = event.event_type,
        payload=event.model_dump_json()
    )