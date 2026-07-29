# Reverse Proxy Architecture for a Dockerized EDMS

**Category:** Infrastructure

## Overview
A Mayan EDMS deployment (s4.9) on a cloud VPS (15 GB RAM, 96 GB disk) needed a unified HTTP entry point to serve its Dockerized Django backend, REST API, static assets, and a React frontend — all through a single Nginx reverse proxy.

## Problem
The EDMS ran as a set of Docker containers — Mayan EDMS (Django/Gunicorn) on port 8000, PostgreSQL 14, RabbitMQ 4.0, and Redis 7.4 — each isolated on a Docker bridge network. The Django app required: static assets with long-term caching, a REST API with X-Forwarded-* header preservation, SCRIPT_NAME header for Django sub-path routing at /mayan/, a React SPA at /, and a 200 MB upload limit for document scans.

## Solution
Configured Nginx with a sophisticated multi-location reverse proxy serving as the gateway between public internet and Dockerized microservices. Four distinct location blocks: `/` serves the React SPA via static files, `/static/` proxies to Django with 30-day caching, `/api/` proxies to REST API with full header forwarding, and `/mayan/` proxies to Django with the critical `SCRIPT_NAME /mayan` header for sub-path routing. `client_max_body_size` set to 200 MB. Docker Compose includes Traefik for future production TLS.

## Key Highlights
- 4 distinct Nginx location blocks: / (React SPA), /static/, /api/, /mayan/
- SCRIPT_NAME header for Django sub-path routing behind reverse proxy
- 200 MB upload limit for high-resolution document scans
- 30-day browser cache for static assets
- Full X-Forwarded-* header chain preserved for backend
- Traefik integration planned for production Let's Encrypt TLS

## Tech Stack
Nginx, Mayan EDMS s4.9, Docker, Django, React, Vite, PostgreSQL 14, RabbitMQ 4.0, Redis 7.4, Traefik, Ubuntu 24.04

## Outcome
A single Nginx reverse proxy unifies access to the Dockerized EDMS stack — React SPA for end users, Django backend for document management, REST API for programmatic access, and cached static assets for performance — all behind a 200 MB upload limit and proper header forwarding.

## Lessons Learned
Reverse proxy complexity scales with service diversity. This config required 4 distinct routing strategies: static file serving, transparent proxying with caching, API proxying with header forwarding, and Django sub-path routing with SCRIPT_NAME. The SCRIPT_NAME header was the most critical detail — without it, Django's URL reversal breaks entirely behind a path-prefixed proxy.
