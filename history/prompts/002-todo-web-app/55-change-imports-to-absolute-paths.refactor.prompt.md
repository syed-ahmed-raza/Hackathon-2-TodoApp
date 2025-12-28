---
id: 55
title: Change Imports to Absolute Paths
stage: refactor
date: 2025-12-29
surface: agent
model: gemini-cli
feature: 002-todo-web-app
branch: main
user: unspecified
command: /sp.implement
labels: [refactor, imports]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - backend/src/routes/auth.py
  - backend/src/routes/chat.py
  - backend/src/routes/tasks.py
tests:
  - none
---

## Prompt

The project structure is restored to `backend/src`, but the imports were changed to relative paths (using `.` and `..`).
I need them to be standard absolute imports to run locally easily.

Please MODIFY the files in `backend/src/` as follows:

1. **In `backend/src/main.py`**:
   - Change `from .database import ...` TO `from database import ...`
   - Change `from .routes import ...` TO `from routes import ...`

2. **In `backend/src/routes/*.py`** (auth.py, tasks.py, chat.py):
   - Change `from ..database import ...` TO `from database import ...`
   - Change `from ..auth import ...` TO `from auth import ...`
   - Change `from ..crud import ...` TO `from crud import ...`
   - Change `from .. import models` TO `import models`

Basically, remove the dots so I can run `uvicorn main:app` directly from inside the `src` folder.

## Response snapshot

I have changed the imports from relative to absolute in the specified files.

## Outcome

- ✅ Impact: Imports in `backend/src` are now absolute.
- 🧪 Tests: No tests were run.
- 📁 Files: 4 files were modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The changes were straightforward, replacing relative import syntax with absolute import syntax.
