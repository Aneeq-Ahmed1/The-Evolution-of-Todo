# Research Findings: FastAPI Backend for Todo Application

**Feature**: 1-fastapi-backend
**Date**: 2026-01-05

## Research Summary

This document captures research findings and technical decisions made during the planning phase for the FastAPI backend implementation.

## Decision: JWT Implementation with PyJWT
**Rationale**: The specification requires JWT verification using PyJWT. PyJWT is the standard library for handling JWT tokens in Python and integrates well with FastAPI. It supports signature verification, expiration checking, and token decoding as required by the specification.

**Alternatives considered**:
- python-jose: Also supports JWT but PyJWT is more actively maintained
- Authlib: More comprehensive but overkill for simple JWT verification

## Decision: SQLModel for ORM
**Rationale**: The specification explicitly requires SQLModel for the ORM. SQLModel combines the power of SQLAlchemy with Pydantic, providing both database modeling and request/response validation in a single framework.

**Alternatives considered**:
- Pure SQLAlchemy: Would require separate validation library
- Tortoise ORM: Async-native but doesn't integrate with Pydantic as seamlessly

## Decision: Neon Serverless PostgreSQL
**Rationale**: The specification requires Neon Serverless PostgreSQL as the database. Neon provides serverless PostgreSQL with auto-scaling and branch capabilities, making it suitable for the multi-user application.

**Alternatives considered**:
- Standard PostgreSQL: Would require manual scaling
- SQLite: Not suitable for multi-user applications
- MongoDB: Doesn't align with SQLModel requirement

## Decision: Better Auth JWT Compatibility
**Rationale**: The specification requires compatibility with Better Auth issued JWT tokens. Better Auth uses standard JWT format with RS256 or HS256 signing algorithms. The backend must verify tokens issued by Better Auth using the shared secret.

**Alternatives considered**:
- Custom auth system: Would not be compatible with existing frontend
- OAuth providers: Not required by specification

## Decision: Environment Configuration with Settings
**Rationale**: The specification requires reading BETTER_AUTH_SECRET and DATABASE_URL from environment variables. Using a settings module (likely with pydantic's BaseSettings) provides type validation and secure configuration management.

**Alternatives considered**:
- Hardcoded values: Insecure and inflexible
- Configuration files: Less secure than environment variables

## Decision: FastAPI Dependency System for Authentication
**Rationale**: FastAPI's dependency injection system is ideal for implementing JWT verification as a reusable dependency that can be applied to all protected routes. This centralizes authentication logic and ensures consistent security across all endpoints.

**Alternatives considered**:
- Decorators: Less flexible than FastAPI dependencies
- Manual verification in each route: Would lead to code duplication

## Decision: REST API Structure
**Rationale**: The specification defines specific REST endpoints under /api with user_id in the path. This structure provides clear resource organization and enables proper user isolation through the authentication system.

**Alternatives considered**:
- GraphQL: Not specified in requirements
- Different path structure: Would not match specification

## Decision: Error Handling Strategy
**Rationale**: The specification defines specific HTTP status codes for different error conditions (401, 403, 404, 409, 422). Implementing these consistently ensures proper error communication with the frontend and predictable behavior.

**Alternatives considered**:
- Generic error responses: Would not provide specific feedback
- Custom error codes: Would not align with specification