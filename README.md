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

- React, planned for later milestones

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

The project currently has a functional local video processing pipeline and a basic real-time WebSocket streaming API.

Implemented:

- Initial FastAPI API gateway
- Health check endpoint
- Shared configuration module using Pydantic Settings
- Docker Compose setup for local API execution
- Python project tooling with Ruff and pytest
- Editable local installation through pip
- Local video capture from webcam or video files
- YOLO-based frame inference
- Structured detection result schemas
- Optional annotated frame output
- Detection event schemas for real-time messaging
- WebSocket endpoint for detection event streaming
- Local WebSocket debug client
- Basic automated tests for API, video, detection and streaming components

Planned next:

- Redis Streams event pipeline
- Multi-agent pipeline
- Real-time dashboard
- Tracking and activity recognition agents
- Alerting workflow
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

Create a local environment file:

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

The endpoint is intended for local development and debugging before the project introduces a frontend dashboard or a distributed event-driven pipeline.

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

- Detection runs locally in the API process.
- Only local webcam indexes or local video file paths are supported.
- Detection events are streamed as JSON, but annotated frames are not streamed.
- The current implementation does not use Redis Streams yet.
- Multi-agent orchestration is not implemented yet.
- The WebSocket endpoint does not include authentication or production-grade access control yet.

## Testing and Linting

Run tests:

```powershell
pytest
```

Run linting:

```powershell
ruff check .
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
- Video ingestion service
- Detection workers
- Coordinator agent
- Alert agent

### Milestone 5: Dashboard and real-time visualisation

- React dashboard
- Detection display
- Alert feed
- Stream status panel

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
packages/
  shared/
    detection/
    events/
    streaming/
    video/
tests/
docs/
scripts/
```

`apps/` contains application services.

`packages/shared/` contains reusable shared code.

`tests/` contains automated tests.

`docs/` contains technical documentation.

`scripts/` contains utility scripts.

## License

This project is licensed under the MIT License.
