--- 
id: 15
title: Replace OpenAI with Google Gemini in Backend Chat Logic
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: "/sp.implement Replace OpenAI with Google Gemini (Free Tier) in `backend/src/routes/chat.py`."
labels: ["implementation", "backend", "google-gemini", "openai-replacement", "chat-logic"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/routes/chat.py
  - backend/src/crud.py
  - backend/src/auth.py
tests: []
---

## Prompt

```text
/sp.implement Act as a Senior Python Developer.

**Objective:** Replace OpenAI with Google Gemini (Free Tier) in `backend/src/routes/chat.py`.

**Context:** The user has installed `google-generativeai` and set `GEMINI_API_KEY`.

**Action: Completely Rewrite `backend/src/routes/chat.py`**
1.  **Imports:**
    -   `import os`
    -   `import google.generativeai as genai`
    -   `from fastapi import APIRouter, Depends, HTTPException`
    -   `from sqlalchemy.orm import Session`
    -   `from ..database import get_db`
    -   `from ..auth import get_current_user_id`
    -   `from ..crud import create_task, get_tasks, delete_task`
    -   `from pydantic import BaseModel`

2.  **Configuration:**
    -   `genai.configure(api_key=os.getenv("GEMINI_API_KEY"))`

3.  **Request Model:**
    -   `class ChatRequest(BaseModel): message: str`

4.  **Route Definition:**
    -   `router = APIRouter()`
    -   `@router.post("/api/chat")`
    -   `async def chat_agent(request: ChatRequest, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):`

5.  **Inside `chat_agent` (The Logic):**
    -   **Define Tool Wrappers:** Create internal functions inside `chat_agent` so they can access `db` and `current_user_id`. Add docstrings so Gemini knows how to use them.
        -   `def add_my_task(title: str): """Adds a task.""" create_task(db, title, "Pending", current_user_id); return "Task added."`
        -   `def get_my_tasks(): """Gets all tasks.""" tasks = get_tasks(db, current_user_id); return str([t.title for t in tasks])`
        -   `def delete_my_task(task_id: int): """Deletes a task by ID.""" delete_task(db, task_id, current_user_id); return "Task deleted."`
    -   **Initialize Model:** `model = genai.GenerativeModel("gemini-1.5-flash", tools=[add_my_task, get_my_tasks, delete_my_task])`
    -   **Start Chat:** `chat = model.start_chat(enable_automatic_function_calling=True)`
    -   **Send Message:** `response = chat.send_message(request.message)`
    -   **Return:** `return response.text`

**Output:**
Confirm when the file is rewritten.
```

## Response snapshot

```text
Successfully created and wrote to new file: D:\My Work\Coding\Governor Course\Q4\hackathon 2 todo list\backend\src\crud.py.
Successfully modified file: D:\My Work\Coding\Governor Course\Q4\hackathon 2 todo list\backend\src\routes\chat.py (1 replacements).
Successfully overwrote file: D:\My Work\Coding\Governor Course\Q4\hackathon 2 todo list\backend\src\routes\chat.py.
Successfully modified file: D:\My Work\Coding\Governor Course\Q4\hackathon 2 todo list\backend\src\auth.py (1 replacements).
```

## Outcome

- ✅ Impact: Successfully replaced OpenAI integration with Google Gemini in the backend chat logic. This involved creating a new `crud.py` file to centralize database operations, rewriting `backend/src/routes/chat.py` with Gemini-specific imports, configuration, tool wrappers, and chat handling logic, and modifying `backend/src/auth.py` to correctly provide the `user_id` for these operations.
- 🧪 Tests: No explicit tests were added. Verification would involve running the backend, ensuring `GEMINI_API_KEY` is set, and testing the chat functionality through the frontend to confirm Gemini's responses and tool executions.
- 📁 Files: Created `backend/src/crud.py`, completely rewrote `backend/src/routes/chat.py`, and modified `backend/src/auth.py`.
- 🔁 Next prompts: The backend is now configured for Gemini. The next steps could involve ensuring the frontend properly sends `GEMINI_API_KEY` or verifying all API interactions work as expected.
- 🧠 Reflection: The task required careful refactoring of database operations into a new `crud` module, which was a necessary step for cleaner architecture and to accommodate Gemini's tool calling mechanism. The dynamic definition of tool wrappers within the endpoint function allows access to the `db` session and `user_id`.

## Evaluation notes (flywheel)

- Failure modes observed: Initial ambiguity regarding `crud.py` was resolved by creating the file and moving functions.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
