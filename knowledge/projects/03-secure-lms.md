# Secure Learning Management System

**Category:** Backend Engineering
**Status:** Completed

## Description
Co-developed a grades portal and learning platform with FastAPI backend and React frontend. Implemented JWT authentication with OTP verification for multi-factor access, role-based authorization (admin, teacher, student), and secure REST APIs with input validation. The React frontend provides separate dashboards for each user role with tailored views and secure API consumption.

## Architecture Decisions
- JWT + OTP for multi-factor authentication
- Role-based access control with three tiers — each with distinct frontend views
- PostgreSQL for production with Alembic-managed schema migrations
- bcrypt for password hashing
- React frontend with role-aware routing and conditional rendering

## Tech Stack
FastAPI, React.js, TypeScript, PostgreSQL, JWT, Alembic, SQLAlchemy, bcrypt

## Highlight
Multi-factor authentication with JWT + OTP and role-based access control

## Repository
github.com/Wesley534/secure_lms (private)
