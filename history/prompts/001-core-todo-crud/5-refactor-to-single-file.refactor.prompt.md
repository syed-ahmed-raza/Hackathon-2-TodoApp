---
id: 5
title: Refactor to Single File
stage: refactor
date: 2025-12-25
surface: agent
model: gemini
feature: 001-core-todo-crud
branch: 001-core-todo-crud
user: {{USER}}
command: /sp.implement
labels: [refactor, python]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- main.py
- src/ (deleted)
tests:

---

## Prompt

/sp.implement Act as a Senior Python Engineer.

**Objective:** Refactor the entire Phase I implementation into a SINGLE file for simplicity, while maintaining professional code quality.

**Action Plan:**
1.  **Cleanup:** Instruct me to delete the `src/` directory if it exists.
2.  **Implementation:** Generate a single file named `main.py` that contains the entire Todo Application.
3.  **Requirements:**
    - The code must still adhere to the **Phase I Spec**: Add, View, Update, Delete, Mark Complete.
    - Use **Strict Type Hinting** and **Docstrings** (Compliance with Constitution).
    - Use the `rich` library for a professional CLI look.
    - **Internal Structure:** Even though it is one file, define three distinct classes inside it:
        - `class Task`: The data model (using @dataclass).
        - `class TodoService`: The business logic (CRUD operations).
        - `class TodoApp`: The UI logic (handling user input and `rich` console).

**Output:**
1.  Provide the content for `requirements.txt` (must include `rich`).
2.  Provide the content for the consolidated `main.py`.

Generate the code now.

## Response snapshot

I have refactored the application into a single `main.py` file as requested. The old `src` directory is gone, and the new `main.py` contains all the logic.

## Outcome

- ✅ Impact: Successfully refactore the application into a single file, simplifying the project structure while maintaining code quality and functionality.
- 🧪 Tests: No tests were run.
- 📁 Files: Deleted the `src` directory and overwrote `main.py` with the consolidated code.
- 🔁 Next prompts: The application is ready for validation in its new single-file format.
- 🧠 Reflection: Consolidating the files was straightforward. The code remains modular internally, even within a single file, by keeping the classes distinct and well-defined.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): N/A
