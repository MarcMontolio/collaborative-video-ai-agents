export interface AlertEvent {
  event_type: string;
  timestamp: string;
  severity: string;
  message: string;
  source: string | null;
  frame_index: number | null;
  detected_classes: string[];
}
