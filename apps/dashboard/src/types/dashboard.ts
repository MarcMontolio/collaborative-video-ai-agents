import type { AlertEvent } from "./alert";
import type { DetectionEvent } from "./detection";


export type DashboardEvent =
    | {
        type: 'detection'
        payload: DetectionEvent
    }
    | {
        type: 'alert'
        payload: AlertEvent
    }