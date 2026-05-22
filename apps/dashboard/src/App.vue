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
