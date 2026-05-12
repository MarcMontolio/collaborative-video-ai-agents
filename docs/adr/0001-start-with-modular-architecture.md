# ADR-0001: Start with a modular architecture

## Status

Accepted

## Context

The project aims to become a distributed real-time video analysis platform based on specialised AI agents.

The planned system includes multiple responsibilities such as video ingestion, object detection, person detection, tracking, activity recognition, coordination, alerting and real-time API communication.

Starting directly with fully separated microservices would add operational complexity before the core video analysis flow has been validated. It would require service orchestration, inter-service communication, container networking, local development conventions and deployment concerns from the beginning.

At this stage, the project needs a structure that keeps responsibilities separated without slowing down the first functional implementation.

## Decision

The project will start with a modular architecture inside a single repository.

Application services will live under `apps/`, while reusable shared code will live under `packages/shared/`.

The initial implementation can run as a small FastAPI-based foundation, while keeping the code organised so that future services and agents can be separated progressively.

The project will not start as a full microservices system from day one.

## Consequences

This approach reduces initial complexity and allows the first functional version to be built faster.

It keeps the project easier to run, test and understand during the foundation and MVP stages.

The codebase still preserves clear boundaries between application services and shared modules, which prepares the project for future extraction into independent workers or services.

The main trade-off is that the first implementation is not fully distributed yet. Service separation, independent scaling and stronger runtime isolation will be added progressively once the core pipeline is working.
