# Collaborative Real-Time Video Analysis with AI Agents

Project to create a real-time video analysis platform using collaborative AI agents, FastAPI, OpenCV, YOLO, Redis Streams and WebSockets.

## Overview

This project intends to be a real-time video analysis platform based on a multi-agent architecture.

The system will divide video processing into specialised agents: video ingestion, person detection, object detection, tracking, activity recognition, coordination and alerts.

The main objective is to build a functional version first and then progressively evolve it into a distributed, observable and scalable architecture.

## Goals

- [ ] Analyse real-time video.
- [ ] Separate responsibilities across specialised agents.
- [ ] Design an event-driven architecture.
- [ ] Process frames concurrently.
- [ ] Expose results via API and WebSockets.
- [ ] Visualise detections and alerts in a dashboard.
- [ ] Add observability, metrics and structured logging.
- [ ] Maintain a professional and extensible project structure.

## Planned Tech Stack

### Backend

- Python 3.12
- FastAPI
- Pydantic Settings
- Uvicorn

### Video and AI

- OpenCV
- YOLO
- Future tracking/activity recognition components

### Messaging and Real-Time Communication

- Redis Streams
- WebSockets
- RabbitMQ or Kafka as future options

### Infrastructure

- Docker
- Docker Compose

### Frontend

- Vue 3
- Vite
- TypeScript

### Quality and Tooling

- pytest
- Ruff
- GitHub Actions, planned

## Architecture Overview

```text
Video Source
    |
    v
Video Ingestion Service
    |
    v
Event Bus
    |
    +--> Person Detection Agent
    +--> Object Detection Agent
    +--> Tracking Agent
    +--> Activity Recognition Agent
    |
    v
Coordinator Agent
    |
    +--> Alert Agent
    +--> API Gateway
    |
    v
Dashboard
```

The architecture is designed around specialised agents that communicate through events. Each agent owns a specific responsibility and can later be scaled or replaced independently.

The first implementation starts with a small FastAPI-based foundation and will progressively evolve into a distributed pipeline.

## Current Project Status

The project currently has a functional local video processing pipeline, a real-time WebSocket streaming API, an initial Redis Streams event-driven pipeline and a Vue dashboard for real-time visualisation.

Implemented:

- Initial FastAPI API gateway
- Health check endpoint
- Shared configuration module using Pydantic Settings
- Docker Compose setup for local API and Redis execution
- Python project tooling with Ruff and pytest
- Editable local installation through pip
- Local video capture from webcam or video files
- YOLO-based frame inference
- Structured detection result schemas
- Optional annotated frame output
- Detection event schemas for real-time messaging
- WebSocket endpoint for detection event streaming
- Local WebSocket debug client
- Redis client configuration
- Redis Streams publisher for detection events
- Redis Streams consumer for detection events
- Detection event coordinator and summary generation
- Alert event schema and simple alert publisher
- Unified dashboard WebSocket endpoint for detection and alert events
- Vue dashboard scaffold
- Dashboard WebSocket integration
- Live detection event display
- Stream controls for source, model path, frame step and max frames
- Run-until-disconnected stream mode
- Live stream summary panel
- Person alert feed connected to backend-generated alert events
- Basic dashboard metrics
- Basic automated tests for API, video, detection, streaming, Redis, coordinator and alert components

Planned next:

- Tracking and activity recognition agents
- More advanced alerting rules
- Annotated video visualization
- Observability, metrics and structured logging

## Local Development

### Requirements

- Python 3.12
- pip
- Docker and Docker Compose, for containerised execution

### Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Running the API locally

Start the API gateway:

```powershell
uvicorn apps.api_gateway.main:app --reload
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "api-gateway"
}
```

## Running with Docker Compose

Optionally, create a local environment file:

```powershell
Copy-Item .env.example .env
```

Start the API gateway:

```powershell
docker compose up --build
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "api-gateway"
}
```

## Real-time detection streaming

The API gateway exposes a WebSocket endpoint for streaming detection events generated from a local video source or webcam.

The endpoint is intended for local development, debugging and detection-only streaming. The Vue dashboard uses `/ws/dashboard`, which streams both detection and alert messages through a unified WebSocket flow.

### WebSocket endpoint

```text
ws://127.0.0.1:8000/ws/detections
```

The endpoint accepts the following query parameters:

- `source`: webcam index or local video path. Default: `0`.
- `model_path`: YOLO model path or model name. Default: `yolo11n.pt`.
- `frame_step`: process every N frames. Default: `5`.
- `max_frames`: optional frame limit. Default: unlimited.

Example:

```text
ws://127.0.0.1:8000/ws/detections?source=0&model_path=yolo11n.pt&frame_step=5&max_frames=20
```

### Debug WebSocket client

A lightweight debug client is available for testing the detection WebSocket endpoint without a frontend dashboard.

Start the API first:

```powershell
uvicorn apps.api_gateway.main:app --reload
```

Then run the debug client:

```powershell
python scripts\debug_websocket_client.py --url "ws://127.0.0.1:8000/ws/detections?source=0&model_path=yolo11n.pt&frame_step=5&max_frames=20"
```

The client connects to the WebSocket endpoint and prints received detection events to the console.

If the API is not running or cannot be reached, the client prints a clear connection error message.

### Current limitations

The current WebSocket streaming implementation is intended for local development and debugging.

Known limitations:

- Detection runs locally in the API process for the WebSocket endpoint.
- Only local webcam indexes or local video file paths are supported.
- Detection events are streamed as JSON, but annotated frames are not streamed.
- The detection-only WebSocket endpoint is separate from the Redis Streams pipeline for now.
- The dashboard uses a unified WebSocket endpoint for local visualisation.
- Multi-agent orchestration is still limited to local modules and scripts.
- The WebSocket endpoint does not include authentication or production-grade access control yet.

## Dashboard

The project includes a Vue dashboard for visualising real-time detection events, person alerts, stream status and basic session metrics.

The dashboard connects to the backend through a unified WebSocket endpoint that streams both detection events and generated alert events from a single video processing flow.

### Frontend setup

Install dashboard dependencies:

```powershell
cd apps\dashboard
npm install
```

Build the dashboard:

```powershell
npm run build
```

Return to the repository root when needed:

```powershell
cd ..\..
```

### Running the dashboard locally

Start the backend API from the repository root:

```powershell
uvicorn apps.api_gateway.main:app --reload
```

Start the dashboard in another terminal:

```powershell
cd apps\dashboard
npm run dev
```

The dashboard is served by Vite, usually at:

```text
http://127.0.0.1:5173
```

or:

```text
http://localhost:5173
```

### Dashboard WebSocket endpoint

The dashboard uses the following backend endpoint:

```text
ws://127.0.0.1:8000/ws/dashboard
```

This endpoint streams dashboard messages using a simple envelope format:

```json
{
  "type": "detection",
  "payload": {}
}
```

or

```json
{
  "type": "alert",
  "payload": {}
}
```

Detection messages update the live detection event list and dashboard metrics.

Alert messages update the person alert feed.

### Stream controls

The dashboard provides controls for:

- `source`: webcam index or local video path. Default: `0`.
- `model_path`: YOLO model path or model name. Default: `yolo11n.pt`.
- `frame_step`: process every N frames. Default: `5`.
- `max_frames`: optional frame limit.
- `Run until disconnected`: omits `max_frames` and keeps the stream running until the user disconnects, refreshes the page or the source ends.

The generated WebSocket URL is displayed in the dashboard before connecting.

### Dashboard features

The current dashboard includes:

- Live detection event list
- Detected class and confidence display
- Source and processing time display
- Live summary panel
- Person alert feed
- Session-level metrics
- Connect and disconnect actions
- Run-until-disconnected mode

Current metrics include:

- Total detection events
- Total detections
- Latest processed frame
- Average processing time
- Person alerts

### Current limitations

The dashboard is intended for local development and portfolio demonstration.

Known limitations:

- The dashboard does not stream annotated video frames yet.
- Detection runs locally in the backend API process.
- Browser clients do not connect directly to Redis Streams.
- Dashboard metrics are session-level and reset when the page reloads.
- The alert feed currently focuses on person detections.
- The dashboard does not include authentication or production-grade access control yet.

## Event-driven Redis Streams pipeline

The project includes an initial Redis Streams pipeline for moving detection events between independent components.

This pipeline is intended to prepare the project for a future multi-agent architecture where ingestion, detection, coordination and alerting can run as separate services or workers.

### Pipeline flow

```text
Local video source
    |
    v
YOLO detection stream
    |
    v
DetectionEvent
    |
    v
Redis Stream: detection-events
    |
    v
Detection consumer worker
    |
    v
DetectionSummary
    |
    v
AlertEvent
    |
    v
Redis Stream: alert-events
```

The detection publishing and detection consuming steps can be run locally with the scripts below.

The coordinator and alert publisher are implemented as shared modules. The Vue dashboard currently receives backend-generated alerts through `/ws/dashboard`, while the Redis alert stream remains reserved for event-driven worker-based alert publishing.

### Redis Streams

The project currently uses the following Redis Streams:

```text
detection-events
alert-events
```

`detection-events` stores detection events generated from local video processing.
`alert-events` is reserved for alert events generated from detection summaries in the Redis-based pipeline. The dashboard currently receives alert events through the backend `/ws/dashboard` endpoint instead of reading Redis Streams directly.

### Running Redis locally

Start Redis with Docker Compose:

```powershell
docker compose up redis
```

To start the full local stack:

```powershell
docker compose up --build
```

### Publishing detection events to Redis

Start Redis first, then publish detection events from a local video source or webcam:

```powershell
python scripts\publish_detection_events.py --source 0 --model yolo11n.pt --frame-step 5 --max-frames 20
```

The script runs local detection processing and publishes generated detection events to the `detection-events` Redis Stream.

### Consuming detection events from Redis

After publishing detection events, consume them with:

```powershell
python scripts\consume_detection_events.py --last-id 0 --count 10
```

The consumer reads detection events from Redis, parses them back into structured `DetectionEvent` objects and prints a short summary for each event.

### Inspecting Redis Streams manually

You can inspect detection events with:

```powershell
docker exec -it collaborative-video-redis redis-cli XRANGE detection-events - +
```

You can inspect alert events with:

```powershell
docker exec -it collaborative-video-redis redis-cli XRANGE alert-events - +
```

### Current limitations

The current Redis Streams pipeline is intended for local development and architecture validation.

Known limitations:

- Redis Streams are used without consumer groups for now.
- Detection publishing currently runs from a local script.
- The consumer worker is a local debugging worker, not a long-running production service.
- Alert generation currently uses a simple person-detection rule based on detection summaries.
- Advanced alert rules, tracking and activity recognition are not implemented yet.
- Alert schemas and publishing helpers exist, but alert publishing is not yet wired into a runnable worker script.
- Backpressure, retries and dead-letter handling are not implemented yet.

## Testing and Linting

Run tests:

```powershell
pytest
```

Run linting:

```powershell
ruff check .
```

Run dashboard build:

```powershell
cd apps\dashboard
npm run build
cd ..\..
```

## Roadmap

### Milestone 1: Project foundation

- Project structure
- Python tooling
- FastAPI health endpoint
- Shared configuration
- Docker Compose setup
- Initial README
- Basic CI workflow
- Initial architecture decision records

### Milestone 2: Local video processing

- Read video from file or webcam
- Extract frames with OpenCV
- Run YOLO inference
- Produce structured detection results
- Save optional annotated frames
- Add basic tests for video and detection components

### Milestone 3: Real-time API and WebSocket streaming

- Detection event schemas
- WebSocket endpoint
- Live detection result streaming
- Basic debug client
- Real-time streaming usage documentation

### Milestone 4: Event-driven multi-agent pipeline

- Redis Streams integration
- Redis client configuration
- Detection event publisher
- Detection stream consumer worker
- Coordinator agent
- Alert event schema
- Simple alert publisher
- Event-driven pipeline documentation

### Milestone 5: Dashboard and real-time visualisation

- Vue dashboard
- Unified dashboard WebSocket integration
- Live detection display
- Person alert feed
- Stream controls
- Live summary panel
- Basic dashboard metrics
- Dashboard usage documentation

### Milestone 6: Observability, scaling and production readiness

- Structured logging
- Metrics
- Grafana dashboard
- Backpressure strategy
- Scaling documentation

## Repository Structure

```text
apps/
  api_gateway/
  dashboard/
packages/
  shared/
    alerts/
    coordinator/
    detection/
    events/
    redis/
    streaming/
    video/
tests/
docs/
scripts/
```

`apps/` contains application services, including the FastAPI API gateway and the Vue dashboard.

`packages/shared/` contains reusable shared code.

`tests/` contains automated tests.

`docs/` contains technical documentation.

`scripts/` contains utility scripts.

## License

This project is licensed under the MIT License.
