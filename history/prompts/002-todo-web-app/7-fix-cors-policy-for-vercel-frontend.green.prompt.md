---
id: 7
title: Fix CORS Policy for Vercel Frontend
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: /sp.implement Fix the CORS policy blocking the Vercel Frontend.
labels: [implementation, backend, cors-config]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
tests: []
---

## Prompt

```text
/sp.implement Act as a Senior Backend Developer.

**Objective:** Fix the CORS policy blocking the Vercel Frontend.

**Diagnosis:**
The Frontend (Vercel) is trying to call the Backend (Render), but the Backend's `CORSMiddleware` is configured too strictly (likely only allowing localhost).

**Action:**
Update `backend/src/main.py`:
1.  Locate the `CORSMiddleware` configuration.
2.  Change `allow_origins` to allow ALL origins: `allow_origins=["*"]`.
3.  Ensure `allow_credentials=True`, `allow_methods=["*"]`, and `allow_headers=["*"]` are set.
4.  This allows the Vercel deployment to communicate with the Render backend.

**Output:**
Provide the corrected code for `backend/src/main.py`.
```

## Response snapshot

```text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .routes import auth, tasks

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(tasks.router)
```

## Outcome

- ✅ Impact: Successfully configured the backend's `CORSMiddleware` to allow all origins, resolving potential CORS issues for the Vercel Frontend deployment.
- 🧪 Tests: No new tests were added as this was a configuration change. Existing API tests should continue to function correctly.
- 📁 Files: Modified `backend/src/main.py`.
- 🔁 Next prompts: None for this specific task. The user can now proceed with testing the communication between the Vercel frontend and Render backend.
- 🧠 Reflection: The CORS policy was too restrictive, preventing the Vercel frontend from communicating with the backend. Updating `allow_origins` to `["*"]` provides the necessary access.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
