# ADR-0003: Prioritise a functional MVP before optimisation

## Status

Accepted

## Context

The project has several ambitious goals: real-time video processing, AI-based detection, multi-agent coordination, event-driven communication, WebSocket streaming, a dashboard, alerts, observability and future scaling.

Trying to optimise all these areas from the beginning would increase complexity before proving that the basic user-facing flow works.

For a portfolio project, it is important to deliver a working and demonstrable system early. A simple but functional pipeline is more valuable than a highly abstract architecture that cannot yet process video end to end.

The first priority is to validate the core flow: ingest video, process frames, produce detection results, expose them through the API and later stream them in real time.

## Decision

The project will prioritise a functional MVP before advanced optimisation.

Initial implementations may use simple approaches for frame processing, detection orchestration and local execution.

Performance-focused features such as batching, backpressure, frame dropping, advanced model optimisation, worker autoscaling and detailed pipeline metrics will be added progressively after the core pipeline is working.

## Consequences

This approach allows the project to reach a demonstrable state earlier.

It reduces the risk of spending too much time on infrastructure before validating the actual video analysis workflow.

It also makes the project easier to explain and defend, because each optimisation can be introduced as a response to a real bottleneck observed in the system.

The main trade-off is that early versions may not be highly optimised or production-ready. This is acceptable because the roadmap explicitly includes later work on performance, observability and scaling.
