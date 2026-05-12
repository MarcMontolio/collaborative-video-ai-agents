from time import perf_counter

from cv2.typing import MatLike
from ultralytics import YOLO

from packages.shared.detection.schemas import (
    BoundingBox,
    DetectionResult,
    FrameDetectionResult,
)


class YoloDetector:
    def __init__(self, model_path: str = "yolo11n.pt") -> None:
        self.model_path = model_path
        self.model = YOLO(model_path)
        
    def detect(self, frame: MatLike, frame_index: int) -> FrameDetectionResult:
        start_time = perf_counter()
        
        results = self.model(frame, verbose=False)
        result = results[0]
        
        detections: list[DetectionResult] = []
        
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().tolist()
            confidences = result.boxes.conf.cpu().tolist()
            class_ids = result.boxes.cls.cpu().tolist()
            
            for box, confidence, class_id in zip(
                boxes,
                confidences,
                class_ids,
                strict=True):
                x1, y1, x2, y2 = box
                class_name = result.names[int(class_id)]
                
                detections.append(
                    DetectionResult(
                        class_name=class_name,
                        confidence=confidence,
                        bounding_box=BoundingBox(
                            x1=float(x1),
                            y1=float(y1),
                            x2=float(x2),
                            y2=float(y2),
                        ),
                    )
                )
        
        processing_time_ms = (perf_counter() - start_time) * 1000
        
        return FrameDetectionResult(
            frame_index=frame_index,
            detections=detections,
            processing_time_ms=processing_time_ms
        )