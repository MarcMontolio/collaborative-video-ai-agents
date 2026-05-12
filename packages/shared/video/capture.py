import cv2
from cv2.typing import MatLike
from pydantic import BaseModel, Field


class VideoMetadata(BaseModel):
    width: int = Field(ge=0)
    height: int = Field(ge=0)
    fps: float = Field(ge=0)
    frame_count: int | None = Field(ge=0)


class LocalVideoCapture:
    def __init__(self, source: str | int) -> None:
        self.source = source
        self._capture = cv2.VideoCapture(source)
        
        if not self._capture.isOpened():
            raise ValueError(f"Video source cannot be opened {source}")
        
    @property
    def metadata(self) -> VideoMetadata:
        frame_count = int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))
        
        return VideoMetadata(
            width=int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            fps=float(self._capture.get(cv2.CAP_PROP_FPS)),
            frame_count=frame_count if frame_count >= 0 else None 
        )
        
    def read_frame(self) -> tuple[bool, MatLike | None]:
        success, frame = self._capture.read()
        
        if not success:
            return False, None
        
        return True, frame
    
    def release(self) -> None:
        self._capture.release()