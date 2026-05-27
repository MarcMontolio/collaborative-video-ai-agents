<script setup lang="ts">
import { computed, ref } from "vue";

import { createDashboardWebSocket } from "./services/dashboardWebSocket";
import type { AlertEvent } from "./types/alert";
import type { DetectionEvent } from "./types/detection";

const projectName = "Collaborative Real-Time Video Analysis";

const source = ref("0");
const modelPath = ref("yolo11n.pt");
const frameStep = ref(5);
const maxFrames = ref<number | null>(20);
const websocketBaseUrl = "ws://127.0.0.1:8000/ws/dashboard";

const websocketUrl = computed(() => {
  const params = new URLSearchParams({
    source: source.value,
    model_path: modelPath.value,
    frame_step: frameStep.value.toString(),
  });

  if (maxFrames.value !== null) {
    params.set("max_frames", maxFrames.value.toString());
  }

  return `${websocketBaseUrl}?${params.toString()}`;
});

const connectionStatus = ref<
  "disconnected" | "connecting" | "connected" | "error"
>("disconnected");
const receivedEvents = ref<DetectionEvent[]>([]);

const alerts = ref<AlertEvent[]>([]);

let socket: WebSocket | null = null;

function connectToDetectionStream() {
  if (frameStep.value < 1) {
    connectionStatus.value = "error";
    return;
  }

  if (maxFrames.value !== null && maxFrames.value < 0) {
    connectionStatus.value = "error";
    return;
  }

  if (socket !== null) {
    socket.close();
  }

  connectionStatus.value = "connecting";

  const currentSocket = createDashboardWebSocket(websocketUrl.value, {
    onOpen: () => {
      if (socket !== currentSocket) {
        return;
      }

      connectionStatus.value = "connected";
    },
    onMessage: (event) => {
      if (socket !== currentSocket) {
        return;
      }

      if (event.type === "detection") {
        receivedEvents.value = [event.payload, ...receivedEvents.value].slice(
          0,
          10,
        );
        return;
      }

      if (event.type === "alert") {
        alerts.value = [event.payload, ...alerts.value].slice(0, 10);
        return;
      }
    },
    onError: () => {
      if (socket !== currentSocket) {
        return;
      }

      connectionStatus.value = "error";
    },
    onClose: () => {
      if (socket !== currentSocket) {
        return;
      }

      connectionStatus.value = "disconnected";
      socket = null;
    },
  });

  socket = currentSocket;
}

function disconnectFromDetectionStream() {
  socket?.close();
  socket = null;
  connectionStatus.value = "disconnected";
}
</script>

<template>
  <main class="dashboard">
    <section class="hero">
      <p class="eyebrow">Dashboard</p>
      <h1>{{ projectName }}</h1>
      <p class="description">
        Real-time detection events, stream status and alerts will be displayed
        here.
      </p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Detection Stream</h2>
        <p>
          Connect to the backend WebSocket endpoint and receive detection
          events.
        </p>

        <div class="connection-panel">
          <div class="control-grid">
            <label>
              Source
              <input v-model="source" type="text" />
            </label>

            <label>
              Model path
              <input v-model="modelPath" type="text" />
            </label>

            <label>
              Frame step
              <input v-model.number="frameStep" min="1" type="number" />
            </label>

            <label>
              Max frames
              <input v-model.number="maxFrames" min="0" type="number" />
            </label>
          </div>

          <div class="websocket-preview">
            <span>WebSocket URL</span>
            <code>{{ websocketUrl }}</code>
          </div>

          <div class="actions">
            <button type="button" @click="connectToDetectionStream">
              Connect
            </button>
            <button type="button" @click="disconnectFromDetectionStream">
              Disconnect
            </button>
          </div>

          <p class="status">Status: {{ connectionStatus }}</p>
          <p class="status">Received events: {{ receivedEvents.length }}</p>
          <div class="event-list">
            <article
              v-for="event in receivedEvents"
              :key="`${event.timestamp}-${event.detection_result.frame_index}`"
              class="event-item"
            >
              <div class="event-header">
                <strong>Frame {{ event.detection_result.frame_index }}</strong>
                <span
                  >{{
                    event.detection_result.detections.length
                  }}
                  detection(s)</span
                >
              </div>

              <p class="event-meta">Source: {{ event.source ?? "unknown" }}</p>

              <p class="event-meta">
                Processing time:
                {{
                  event.detection_result.processing_time_ms === null
                    ? "unknown"
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
        <h2>Live Summary</h2>
        <p>Latest information received from the detection stream.</p>

        <div class="status-summary">
          <p>Status: {{ connectionStatus }}</p>
          <p>Recent events kept: {{ receivedEvents.length }}</p>
          <p>
            Latest frame:
            {{
              receivedEvents.length > 0
                ? receivedEvents[0].detection_result.frame_index
                : "none"
            }}
          </p>
          <p>
            Latest detections:
            {{
              receivedEvents.length > 0
                ? receivedEvents[0].detection_result.detections.length
                : 0
            }}
          </p>
          <p>
            Latest processing time:
            {{
              receivedEvents.length > 0 &&
              receivedEvents[0].detection_result.processing_time_ms !== null
                ? `${receivedEvents[0].detection_result.processing_time_ms.toFixed(2)} ms`
                : "unknown"
            }}
          </p>
        </div>
      </article>

      <article class="card">
        <h2>Alerts</h2>
        <p>
          Alert events generated from detection summaries will be shown here.
        </p>

        <div v-if="alerts.length > 0" class="alert-list">
          <article
            v-for="alert in alerts"
            :key="`${alert.timestamp}-${alert.message}`"
            class="alert-item"
          >
            <div class="alert-header">
              <strong>{{ alert.severity }}</strong>
              <span>{{ alert.event_type }}</span>
            </div>

            <p class="alert-message">{{ alert.message }}</p>

            <p class="alert-meta">Source: {{ alert.source ?? "unknown" }}</p>

            <p class="alert-meta">
              Frame: {{ alert.frame_index ?? "unknown" }}
            </p>

            <p class="alert-meta">
              Classes:
              {{
                alert.detected_classes.length > 0
                  ? alert.detected_classes.join(", ")
                  : "none"
              }}
            </p>
          </article>
        </div>

        <p v-else class="empty-state">No alerts available yet.</p>
      </article>
    </section>
  </main>
</template>
