# Deploying Python Computer Vision Services in Docker

**Category:** Infrastructure

## Overview
Python computer vision dependencies (MediaPipe, DeepFace, OpenCV) had conflicting system requirements and produced 'Illegal instruction' errors across different CPU architectures. Needed containerization for reproducible deployments.

## Problem
MediaPipe and DeepFace rely on native C++ extensions compiled against specific CPU instruction sets (AVX, SSE). Running these on older or less capable CPUs caused runtime crashes. Virtual environments couldn't isolate the system-level dependencies. Required a containerized solution with precise base image selection.

## Solution
Created Docker containers with carefully selected base images matching the target deployment CPU architecture. Isolated conflicting Python ML dependencies into separate containers. Used multi-stage builds to minimize final image size. Implemented dependency version pinning and tested across different CPU architectures. Configured container resource limits for ML model loading.

## Key Highlights
- Dockerfile optimization for Python ML dependencies
- CPU instruction set compatibility resolution
- Multi-stage builds for smaller images
- Dependency isolation and version pinning
- Container debugging and iteration across architectures

## Tech Stack
Docker, Python, MediaPipe, DeepFace, OpenCV, Linux

## Outcome
Successfully containerized AI services that ran reliably across different environments without 'Illegal instruction' crashes. Reproducible builds with pinned dependencies and architecture-matched base images.

## Lessons Learned
Python ML libraries have complex native dependencies — containerization solves reproducibility but requires careful base image selection. Matching the Docker base image to the target CPU architecture is as important as the Python dependencies themselves.
