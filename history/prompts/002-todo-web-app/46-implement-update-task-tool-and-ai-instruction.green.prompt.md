---
id: 46
title: Implement Update Task Tool and AI Instruction
stage: green
date: 2025-12-27
surface: agent
model: gemini
feature: 002-todo-web-app
branch: master
user: syed-ahmed-raza
command: /sp.implement
labels: ["backend", "feature", "ai", "tool-update", "system-instruction"]
links:
  spec: specs/002-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/routes/chat.py
tests:
  - manual verification of file content
---

## Prompt

```text
/sp.implement Act as a Senior Backend Developer.

**Objective:** Fix the bug where tasks disappear or lose descriptions during updates.
**Cause:** The AI lacks an `update_task` tool and tries to Delete+Recreate tasks, which is risky.

**Action:**
1.  In `backend/src/routes/chat.py`, add a new tool function: `update_my_task`.
2.  Register this tool in the `tools` list.
3.  Update the `system_instruction` to use this tool for renaming and completing tasks.

**Code Specification for `update_my_task`:**
```python
def update_my_task(task_identifier: str, title: str = None, description: str = None, is_completed: bool = None):
    """
    Updates a task's title, description, or status (completed).
    Args:
        task_identifier: The Task ID (int) or Task Name (str).
        title: New title (optional).
        description: New description (optional).
        is_completed: True to mark as Done, False for Pending (optional).
    """
    # Logic:
    # 1. Fetch user tasks.
    # 2. Find task by ID (if int) or Name (case-insensitive).
    # 3. If found:
    #    - Update fields if they are not None.
    #    - Commit changes.
    #    - Return "Success: Task updated ✅."
    # 4. If not found: Return "Error: Task not found ❌."
```
```

## Response snapshot

The agent successfully implemented the `update_my_task` tool function in `backend/src/routes/chat.py`, registered it in the `tools` list, and updated the `system_instruction`. This resolves the bug where tasks were disappearing or losing descriptions during updates by providing the AI with a dedicated tool for modifying existing tasks, thus preventing risky Delete+Recreate attempts.

## Outcome

- ✅ Impact: The AI's ability to manage tasks is significantly enhanced by the new `update_my_task` tool, improving task persistence and data integrity. The system is more robust against accidental data loss during updates.
- 🧪 Tests: Manual verification of the `backend/src/routes/chat.py` file content confirmed the successful addition of the `update_my_task` function, its registration, and the updated `system_instruction`.
- 📁 Files: Modified `backend/src/routes/chat.py`.
- 🔁 Next prompts: The user can now proceed with further development or ask for new features.
- 🧠 Reflection: Introducing specialized tools for AI agents can prevent unintended side effects and improve the reliability of complex operations like task updates.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): None.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Implement comprehensive unit and integration tests for all AI tool functions to ensure their correct behavior and interaction with the database.
