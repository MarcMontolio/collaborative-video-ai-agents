export interface BoundingBox {
  x1: number
  y1: number
  x2: number
  y2: number
}

export interface DetectionResult {
  class_name: string
  confidence: number
  bounding_box: BoundingBox
}

export interface FrameDetectionResult {
  frame_index: number
  detections: DetectionResult[]
  processing_time_ms: number | null
}

export interface DetectionEvent {
  event_type: string
  timestamp: string
  source: string | null
  detection_result: FrameDetectionResult
}