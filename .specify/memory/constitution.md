<!--
Sync Impact Report:

- Version change: 1.0.0 → 2.0.0
- List of modified principles:
  - III. Simplicity (Phase I) → III. Backend Technology Stack
  - IV. User Experience (UX) → IV. Frontend Technology Stack
  - V. Future-Proofing → V. Monorepo Architecture
- Added sections:
  - VI. Authentication and Authorization
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (No changes needed)
  - ✅ .specify/templates/spec-template.md (No changes needed)
  - ✅ .specify/templates/tasks-template.md (No changes needed)
  - ✅ README.md (Updated)
- Follow-up TODOs: None
-->
# Hackathon II: The Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (SDD) Mandate
No code is written without a defined Task ID from `speckit.tasks`. The flow is Always: Specify -> Plan -> Tasks -> Implement. All commits and pull requests must reference their corresponding Task ID.

### II. Code Quality
- **Backend**: All Python code must use strict type hinting (`typing`), follow PEP 8 standards, and include docstrings for all public modules, classes, and functions.
- **Frontend**: All frontend code must be written in TypeScript. Use ESLint and Prettier to enforce consistent code style.

### III. Backend Technology Stack
The backend will be built using Python with the **FastAPI** framework. Data will be managed using **SQLModel** as the ORM. The production database is **Neon Serverless Postgres**, while **SQLite** is to be used for local development and testing.

### IV. Frontend Technology Stack
The frontend will be a single-page application built with **Next.js 16+** (using the App Router). The UI will be styled with **Tailwind CSS**.

### V. Monorepo Architecture
The project is organized as a monorepo with clear separation of concerns:
- `/backend`: Contains all Python FastAPI source code, tests, and dependencies.
- `/frontend`: Contains all Next.js source code, tests, and dependencies.
Code should not be commingled between these directories. Shared utilities are not permitted at this stage.

### VI. Authentication and Authorization
The application must feature robust and secure user authentication. The specific integration method will be determined during the planning phase of the auth feature, but it should be a primary consideration.

## Governance
This Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All pull requests and reviews must verify compliance with these principles.

**Version**: 2.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-26