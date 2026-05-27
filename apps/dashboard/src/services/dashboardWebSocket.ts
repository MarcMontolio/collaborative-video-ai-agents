import type { DashboardEvent } from "../types/dashboard";


export interface DashboardWebSocketHandlers {
    onOpen?: () => void
    onMessage?: (event: DashboardEvent) => void
    onError?: (event: Event) => void
    onClose?: () => void
}

export function createDashboardWebSocket(
    url: string,
    handlers: DashboardWebSocketHandlers = {},
): WebSocket {
    const socket = new WebSocket(url)

    socket.onopen = () => {
        handlers.onOpen?.()
    }

    socket.onmessage = (messageEvent) => {
        const dashboardEvent = JSON.parse(messageEvent.data) as DashboardEvent
        handlers.onMessage?.(dashboardEvent)
    }

    socket.onerror = (event) => {
        handlers.onError?.(event)
    }

    socket.onclose = () => {
        handlers.onClose?.()
    }

    return socket
}