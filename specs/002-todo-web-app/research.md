# Research for Todo Web Application

**Date**: 2025-12-26

## Summary

The technology stack for this feature was pre-defined by the project constitution (v2.0.0). This document confirms the choices and outlines best practices to be followed during implementation.

### Decisions

1.  **Backend Framework**: FastAPI
    -   **Rationale**: Specified in the constitution. It's a modern, high-performance Python web framework.
    -   **Best Practices**: Use dependency injection for managing database sessions and authentication. Structure the application into routers for different concerns (e.g., `tasks`, `auth`).

2.  **ORM**: SQLModel
    -   **Rationale**: Specified in the constitution. It combines Pydantic and SQLAlchemy, providing data validation and ORM features in one library, which works well with FastAPI.
    -   **Best Practices**: Define clear models in `models.py` that serve as both database tables and API schemas.

3.  **Frontend Framework**: Next.js (App Router)
    -   **Rationale**: Specified in the constitution. It's a popular React framework that provides a good developer experience and performance.
    -   **Best Practices**: Utilize server components for data fetching where possible. Co-locate pages, components, and styles within the `app` directory. Create a typed API client for interacting with the backend.

4.  **Authentication**: JWT with Email/Password
    -   **Rationale**: Chosen during the specification phase. It's a standard, stateless authentication method suitable for APIs.
    -   **Best Practices**: Store tokens securely on the client-side (e.g., in a secure, HttpOnly cookie). Implement token refresh mechanisms. Ensure password hashing is done correctly on the server.
