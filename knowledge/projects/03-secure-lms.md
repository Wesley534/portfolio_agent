# Secure Learning Management System

**Category:** Backend Engineering
**Status:** Completed

## Description
Co-developed a grades portal and learning platform with FastAPI backend and React frontend. Implemented JWT authentication with OTP verification for multi-factor access, role-based authorization (admin, teacher, student), and secure REST APIs with input validation.

## Architecture Decisions
- JWT + OTP for multi-factor authentication
- Role-based access control with three tiers
- PostgreSQL for production with Alembic-managed schema migrations
- bcrypt for password hashing

## Tech Stack
FastAPI, React.js, PostgreSQL, JWT, Alembic, SQLAlchemy, bcrypt

## Highlight
Multi-factor authentication with JWT + OTP and role-based access control
