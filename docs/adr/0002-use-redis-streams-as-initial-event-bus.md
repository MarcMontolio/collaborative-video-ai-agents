# ADR-0002: Use Redis Streams as the initial event bus

## Status

Accepted

## Context

The project is designed around a future event-driven multi-agent pipeline.

Video frames, detection results, tracking updates, activity recognition outputs and alerts need to move between different components in a structured way.

Several messaging technologies could be used for this purpose, including Redis Streams, RabbitMQ and Kafka.

Kafka provides strong event streaming capabilities, replay, partitioning and scalability, but it also adds operational complexity. RabbitMQ provides flexible routing and mature queueing patterns, but it introduces another broker to operate and tune.

For the MVP stage, the project needs an event bus that is simple to run locally, easy to integrate with Python and good enough to demonstrate asynchronous communication between agents.

## Decision

The project will use Redis Streams as the initial event bus for the multi-agent pipeline.

Redis Streams will be used to publish and consume events such as frame metadata, detection results, aggregated analysis results and alerts.

Redis consumer groups can be used later to distribute work between multiple workers of the same agent type.

Kafka or RabbitMQ may be evaluated in future milestones if the project requires more advanced event streaming, stronger replay semantics, more complex routing or higher-scale partitioning.

## Consequences

Redis Streams keeps the first event-driven implementation relatively simple and easy to run with Docker Compose.

It allows the project to demonstrate asynchronous communication, consumer groups and event-based processing without introducing Kafka-level operational complexity too early.

The main trade-off is that Redis Streams may not be the best long-term choice for very large-scale video analytics workloads, complex event replay requirements or high-throughput multi-camera deployments.

This decision is appropriate for the MVP and early scaling stages, but it should be reviewed if the system grows beyond the initial portfolio scope.
