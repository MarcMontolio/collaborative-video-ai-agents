from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: float = Field(ge=0)
    y1: float = Field(ge=0)
    x2: float = Field(ge=0)
    y2: float = Field(ge=0)
    

class DetectionResult(BaseModel):
    class_name: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    bounding_box: BoundingBox
    

class FrameDetectionResult(BaseModel):
    frame_index: int = Field(ge=0)
    detections: list[DetectionResult] = Field(default_factory=list)
    processing_time_ms: float | None = Field(default=None, ge=0)
    
