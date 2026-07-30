# Connecting Office Scanners to an EDMS

**Category:** Infrastructure

## Overview
A Mayan EDMS deployment (s4.9) on a cloud VPS needed to accept scanned document uploads from physical office scanners on the local network — using SANE (Scanner Access Now Easy) with AirScan/eSCL protocol for network scanner discovery.

## Problem
Physical office scanners on the local network couldn't reliably transfer scanned documents directly into the Mayan EDMS. The scanners supported AirScan (eSCL) and WSD protocols, but the Django backend had no integration layer for real-time scanner communication. The upload pipeline needed to work with the existing Nginx reverse proxy with its multi-route configuration serving a React SPA, Django app under /mayan/, static assets, and REST API.

## Solution
Built a multi-layer document ingestion pipeline: installed sane-utils and sane-airscan on the host for network scanner discovery, bind-mounted a `source_sane_scanners` Mayan app into the Docker container providing a SANE backend. The Nginx reverse proxy was already configured with 4 location blocks (React SPA, Django static assets, REST API, Django sub-path), 200 MB upload limit, and SCRIPT_NAME header for Django routing. Docker Compose includes Traefik for future TLS.

## Key Highlights
- SANE + AirScan (eSCL) network scanner discovery and integration
- source_sane_scanners Mayan app for scanner communication
- Nginx multi-location reverse proxy with 200 MB upload limit
- SCRIPT_NAME header for Django sub-path routing
- Dockerized microservices: Mayan EDMS, PostgreSQL, RabbitMQ, Redis

## Tech Stack
Mayan EDMS s4.9, Nginx, Docker, SANE, AirScan/eSCL, PostgreSQL 14, RabbitMQ 4.0, Redis 7.4, React/Vite, Ubuntu 24.04, Traefik

## Outcome
Physical office scanners can now discover and upload scanned documents directly into the Mayan EDMS through the SANE integration layer. The React frontend provides a modern UI, while the Nginx reverse proxy efficiently routes between services with centralized TLS, header forwarding, and 200 MB upload capacity for high-resolution scans.

## Lessons Learned
Connecting old-protocol hardware (SANE scanners) to modern web applications (Django EDMS) requires bridging multiple integration layers — SANE backend on the host, the Mayan scanner app, the Nginx reverse proxy, and Docker networking. The Nginx config required 4 distinct location blocks, SCRIPT_NAME routing, and a 200 MB limit — highlighting how reverse proxy complexity scales with service diversity.
