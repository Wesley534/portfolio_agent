# Authentication & Authorization Systems

**Category:** Security Engineering
**Status:** Completed

## Description
Designed and implemented secure authentication across multiple applications — JWT with 30-minute token expiry, bcrypt password hashing, OTP verification for multi-factor access, role-based authorization patterns, and API-key secured microservice communication. These patterns are reused across FastAPI, Laravel, and Express backends and integrated with React frontends.

## Architecture Decisions
- JWT with short expiry (30 min) and refresh token rotation
- bcrypt for computationally expensive password hashing
- OTP verification layered on top of JWT for multi-factor access
- Role-based access control (RBAC) with granular permission sets
- API-key authentication for service-to-service communication
- Patterns designed to be framework-agnostic — deployed across FastAPI, Laravel, Express

## Tech Stack
JWT, OAuth 2.0, bcrypt, OTP, RBAC, API Keys, FastAPI, Laravel, Express

## Highlight
Reusable authentication architecture supporting MFA, RBAC, and service-to-service auth
