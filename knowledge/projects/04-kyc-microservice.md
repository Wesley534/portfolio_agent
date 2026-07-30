# KYC Identity Verification Microservice

**Category:** Backend Engineering
**Status:** Completed

## Description
A FastAPI microservice for identity verification using facial recognition and liveness detection. Designed to integrate with a Laravel upstream orchestrator via API-key authentication. Processes biometric data with strict temporary file handling and zero persistent storage of sensitive materials. The Laravel frontend consumes the microservice's REST API endpoints for identity verification workflows.

## Architecture Decisions
- API-key secured microservice architecture
- Temporary file processing — no sensitive data stored
- Laravel orchestrator integration
- Privacy-preserving data handling
- REST API consumed by upstream Laravel frontend

## Tech Stack
FastAPI, Python, REST API, API Security, OpenCV, Laravel

## Highlight
API-key secured microservice architecture with privacy-preserving data handling

## Repository
github.com/Wesley534/kyc_microservice
