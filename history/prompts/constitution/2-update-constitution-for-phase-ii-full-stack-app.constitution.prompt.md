---
id: 2
title: Update Constitution for Phase II Full-Stack App
stage: constitution
date: 2025-12-26
surface: agent
model: gemini-pro
feature: none
branch: main
user: unknown
command: /sp.constitution Act as a Lead System Architect. We are moving to **Phase II: Full-Stack Web Application**.

**Context:**
- Phase I (Console App) is completed and moved to the `phase1_console/` directory. **DO NOT modify or delete anything in `phase1_console/`.**
- We are now building the Phase II Web App in the root directory using a Monorepo structure.

**Update `speckit.constitution` for Phase II:**
1.  **Architecture:** Monorepo Organization.
    - Backend code goes into `/backend`.
    - Frontend code goes into `/frontend`.
2.  **Backend Stack:** Python **FastAPI**, **SQLModel** (ORM), **Neon Serverless Postgres** (or SQLite for local dev).
3.  **Frontend Stack:** **Next.js 16+** (App Router), **Tailwind CSS**.
4.  **Auth:** Better Auth integration.
5.  **SDD Mandate:** Continue Spec-Driven Development. Always reference Task IDs.

Output the updated `speckit.constitution`.
labels: ["architecture", "monorepo", "fastapi", "nextjs"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - README.md
tests:
  null
---

## Prompt

/sp.constitution Act as a Lead System Architect. We are moving to **Phase II: Full-Stack Web Application**.

**Context:**
- Phase I (Console App) is completed and moved to the `phase1_console/` directory. **DO NOT modify or delete anything in `phase1_console/`.**
- We are now building the Phase II Web App in the root directory using a Monorepo structure.

**Update `speckit.constitution` for Phase II:**
1.  **Architecture:** Monorepo Organization.
    - Backend code goes into `/backend`.
    - Frontend code goes into `/frontend`.
2.  **Backend Stack:** Python **FastAPI**, **SQLModel** (ORM), **Neon Serverless Postgres** (or SQLite for local dev).
3.  **Frontend Stack:** **Next.js 16+** (App Router), **Tailwind CSS**.
4.  **Auth:** Better Auth integration.
5.  **SDD Mandate:** Continue Spec-Driven Development. Always reference Task IDs.

Output the updated `speckit.constitution`.

## Response snapshot

Updated the project constitution to version 2.0.0 to reflect the transition to a full-stack web application. Replaced Phase I principles with new ones defining a monorepo architecture, a FastAPI/SQLModel backend, and a Next.js/Tailwind CSS frontend. Also updated the main README.md to describe the new project structure.

## Outcome

- ✅ Impact: Major update to project's guiding principles and developer documentation.
- 🧪 Tests: No tests were run as this was a documentation change.
- 📁 Files: 2 files modified: `.specify/memory/constitution.md`, `README.md`.
- 🔁 Next prompts: `/sp.specify` to begin defining the first feature of the new application.
- 🧠 Reflection: The change correctly captured the user's intent to pivot the project to a full-stack architecture.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment: n/a
