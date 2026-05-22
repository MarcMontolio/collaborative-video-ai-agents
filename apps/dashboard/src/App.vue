<script setup lang="ts">
import { ref } from 'vue'

import { createDetectionWebSocket } from './services/detectionWebSocket'
import type { DetectionEvent } from './types/detection'

const projectName = 'Collaborative Real-Time Video Analysis'
const websocketUrl = ref(
  'ws://127.0.0.1:8000/ws/detections?source=0&model_path=yolo11n.pt&frame_step=5&max_frames=200',
)
const connectionStatus = ref<'disconnected' | 'connecting' | 'connected' | 'error'>(
  'disconnected',
)
const receivedEvents = ref<DetectionEvent[]>([])
let socket: WebSocket | null = null

function connectToDetectionStream() {
  if (socket !== null) {
    socket.close()
  }

  connectionStatus.value = 'connecting'

  const currentSocket = createDetectionWebSocket(websocketUrl.value, {
    onOpen: () => {
      if (socket !== currentSocket) {
        return
      }

      connectionStatus.value = 'connected'
    },
    onMessage: (event) => {
      if (socket !== currentSocket) {
        return
      }

      receivedEvents.value = [event, ...receivedEvents.value].slice(0, 10)
    },
    onError: () => {
      if (socket !== currentSocket) {
        return
      }

      connectionStatus.value = 'error'
    },
    onClose: () => {
      if (socket !== currentSocket) {
        return
      }

      connectionStatus.value = 'disconnected'
      socket = null
    },
  })

  socket = currentSocket
}

function disconnectFromDetectionStream() {
  socket?.close()
  socket = null
  connectionStatus.value = 'disconnected'
}
</script>

<template>
  <main class="dashboard">
    <section class="hero">
      <p class="eyebrow">Dashboard</p>
      <h1>{{ projectName }}</h1>
      <p class="description">
        Real-time detection events, stream status and alerts will be displayed here.
      </p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Detection Stream</h2>
        <p>Connect to the backend WebSocket endpoint and receive detection events.</p>

        <div class="connection-panel">
          <label for="websocket-url">WebSocket URL</label>
          <input id="websocket-url" v-model="websocketUrl" type="text" />

          <div class="actions">
            <button type="button" @click="connectToDetectionStream">Connect</button>
            <button type="button" @click="disconnectFromDetectionStream">
              Disconnect
            </button>
          </div>

          <p class="status">Status: {{ connectionStatus }}</p>
          <p class="status">Received events: {{ receivedEvents.length }}</p>
          <div class="event-lis">
            <article
            v-for="event in receivedEvents"
            :key="`${event.timestamp}-${event.detection_result.frame_index}`"
            class="event-item"
            >
              <div class="event-header">
                <strong>Frame {{ event.detection_result.frame_index}}</strong>
                <span>{{ event.detection_result.detections.length }} detections(s)</span>
              </div>

              <p class="event-meta">
                Source: {{ event.source ?? 'unknown' }}
              </p>

              <p class="event-meta">
                Processing time:
                {{ 
                  event.detection_result.processing_time_ms === null
                  ? 'unknown'
                  : `${event.detection_result.processing_time_ms.toFixed(2)} ms`
                }}
              </p>

              <ul
                v-if="event.detection_result.detections.length > 0"
                class="detection-list"
              >
                <li
                  v-for="detection in event.detection_result.detections"
                  :key="`${detection.class_name}-${detection.confidence}-${detection.bounding_box.x1}-${detection.bounding_box.y1}`"
                >
                  {{ detection.class_name }}
                  <span>{{ (detection.confidence * 100).toFixed(1) }}%</span>
                </li>
              </ul>

              <p v-else class="event-meta">No detections in this frame</p>
            </article>
          </div>
        </div>
      </article>

      <article class="card">
        <h2>Stream Status</h2>
        <p>Connection state and stream controls will be expanded in future issues.</p>
      </article>

      <article class="card">
        <h2>Alerts</h2>
        <p>Alert events generated from detection summaries will be shown here.</p>
      </article>
    </section>
  </main>
</template>
