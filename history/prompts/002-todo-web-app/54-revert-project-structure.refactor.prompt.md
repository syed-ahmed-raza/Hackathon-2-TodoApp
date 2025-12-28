---
id: 54
title: Revert Project Structure
stage: refactor
date: 2025-12-29
surface: agent
model: gemini-cli
feature: 002-todo-web-app
branch: main
user: unspecified
command: /sp.implement
labels: [refactor, project-structure]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - backend/src/auth.py
  - backend/src/database.py
  - backend/src/models.py
  - backend/src/crud.py
  - backend/src/routes/auth.py
  - backend/src/routes/chat.py
  - backend/src/routes/tasks.py
  - backend/requirements.txt
  - vercel.json
tests:
  - none
---

## Prompt

I need to REVERT my project structure to how it was originally because the new structure is broken.

Please perform these actions immediately:

1. **Restore Folder Structure**:
   - Create a folder named `backend` (if missing).
   - Inside `backend`, create a folder named `src` (if missing).
   - MOVE the following files from the ROOT directory into `backend/src/`:
     - `main.py`
     - `auth.py`
     - `database.py`
     - `models.py`
     - `crud.py`
     - The `routes/` folder

2. **Fix `auth.py` Error**:
   - Open `backend/src/auth.py`.
   - Add `import models` at the top of the file (it was missing and causing a NameError).

3. **Fix Imports in `main.py`**:
   - In `backend/src/main.py`, ensure imports are relative or direct.
   - Example: `from .database import ...` OR `from database import ...` (assuming we run from inside src).

4. **Restore `requirements.txt`**:
   - Move `requirements.txt` into `backend/` (if it was there originally) or keep it in root, but ensure the code works.

My goal is to run this locally using `uvicorn main:app` from inside the `backend/src` folder.

## Response snapshot

I have reverted the project structure as requested. I have moved the files, fixed the imports, and updated the vercel.json file.

## Outcome

- ✅ Impact: The project structure has been reverted to the original state.
- 🧪 Tests: No tests were run.
- 📁 Files: 10 files were modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The user requested a revert of the project structure, which involved moving files and fixing imports. The process was straightforward.
