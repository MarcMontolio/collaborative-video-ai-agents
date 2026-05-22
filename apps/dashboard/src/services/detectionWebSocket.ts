import type { DetectionEvent } from '../types/detection'

export interface DetectionWebSocketHandlers {
  onOpen?: () => void
  onMessage?: (event: DetectionEvent) => void
  onError?: (event: Event) => void
  onClose?: () => void
}

export function createDetectionWebSocket(
  url: string,
  handlers: DetectionWebSocketHandlers = {},
): WebSocket {
  const socket = new WebSocket(url)

  socket.onopen = () => {
    handlers.onOpen?.()
  }

  socket.onmessage = (messageEvent) => {
    const detectionEvent = JSON.parse(messageEvent.data) as DetectionEvent
    handlers.onMessage?.(detectionEvent)
  }

  socket.onerror = (event) => {
    handlers.onError?.(event)
  }

  socket.onclose = () => {
    handlers.onClose?.()
  }

  return socket
}