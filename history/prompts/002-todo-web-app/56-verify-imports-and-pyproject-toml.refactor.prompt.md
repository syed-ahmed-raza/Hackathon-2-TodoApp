---
id: 56
title: Verify Imports and pyproject.toml
stage: refactor
date: 2025-12-29
surface: agent
model: gemini-cli
feature: 002-todo-web-app
branch: main
user: unspecified
command: /sp.implement
labels: [refactor, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - pyproject.toml
  - backend/src/main.py
  - backend/src/auth.py
  - backend/src/database.py
  - backend/src/models.py
  - backend/src/crud.py
  - backend/src/routes/auth.py
  - backend/src/routes/chat.py
  - backend/src/routes/tasks.py
tests:
  - none
---

## Prompt

The user wants to FULLY RESTORE the project to its pre-deployment state where everything worked locally.
The folder structure is already back to `backend/src`, but imports are using relative paths (dots) which is causing issues, and `pyproject.toml` might be incorrect.

Please perform these fixes immediately:

1. **Fix Imports in `backend/src/`**:
   - Scan `main.py`, `auth.py`, `database.py`, and all files in `routes/`.
   - REMOVE relative imports. Change them to standard imports.
   - Example: Change `from .database import ...` TO `from database import ...`
   - Example: Change `from ..auth import ...` TO `from auth import ...`
   - Example: Change `from .. import models` TO `import models`

2. **Check & Fix `pyproject.toml`**:
   - Ensure `pyproject.toml` is in the ROOT directory.
   - If it contains a `[tool.uv.workspace]` or similar, ensure it's compatible.
   - If it has script commands, ensure the run command is: `uvicorn main:app --reload` (intended to run from inside `src`).

3. **Cleanup**:
   - If there are any leftover temporary files from the failed restructuring, remove them.

My goal is to `cd backend/src` and run `uvicorn main:app --reload` successfully.

## Response snapshot

I have verified the imports in `backend/src/` are absolute and checked `pyproject.toml`. No further changes were required in this turn.

## Outcome

- ✅ Impact: Project imports and configuration verified.
- 🧪 Tests: No tests were run.
- 📁 Files: No new files were modified in this turn.
- 🔁 Next prompts: none
- 🧠 Reflection: The previous turn correctly addressed the import changes. `pyproject.toml` was confirmed to not require modification for the user's stated goal. No temporary files were identified for cleanup.
