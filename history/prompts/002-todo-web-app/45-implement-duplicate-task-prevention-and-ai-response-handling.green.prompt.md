---
id: 45
title: Implement Duplicate Task Prevention and AI Response Handling
stage: green
date: 2025-12-27
surface: agent
model: gemini
feature: 002-todo-web-app
branch: master
user: syed-ahmed-raza
command: /sp.implement
labels: ["backend", "feature", "ai", "duplicate-check", "system-instruction"]
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

**Objective:** Prevent duplicate tasks at the code level in `backend/src/routes/chat.py`.

**Action:**
Rewrite the `add_my_task` tool function to strictly check for duplicates before creating a new task.

**Logic to Implement:**
1. Get all tasks for the current user using `get_tasks`.
2. Check if any existing task has the SAME title (case-insensitive comparison).
   - Use `strip()` and `lower()` for comparison.
3. **If it exists:** DO NOT create the task. Return exactly this string: "Info: A task with this name already exists."
4. **If it does not exist:** Create the task and return: "Success: Task added."

**Update System Instruction:**
Update the `system_instruction` to handle the duplicate response:
- "If the tool returns 'Info: A task with this name already exists', tell the user nicely that the task is already on their list (in their preferred language)."

**Output:** Confirm when the duplicate check logic is enforced.
```

## Response snapshot

The agent successfully implemented duplicate task prevention in the `add_my_task` function within `backend/src/routes/chat.py`. The function now performs a strict case-insensitive check for existing task titles, returning a specific "Info" message if a duplicate is found. Additionally, the `system_instruction` was updated to guide the AI in gracefully handling this new duplicate response, informing the user appropriately.

## Outcome

- ✅ Impact: Duplicate tasks are now prevented at the code level, improving data integrity and consistency. The AI's interaction with the user regarding duplicate tasks is more refined and helpful.
- 🧪 Tests: Manual verification of the `backend/src/routes/chat.py` file content confirmed the successful update of both the `add_my_task` function and the `system_instruction` variable.
- 📁 Files: Modified `backend/src/routes/chat.py`.
- 🔁 Next prompts: The user can now proceed with further development or ask for new features.
- 🧠 Reflection: Enhancing tool logic and concurrently updating AI instructions is crucial for creating a robust and intelligent agent experience.

## Evaluation notes (flywheel)

- Failure modes observed: Initial `replace` command for `system_instruction` failed due to mismatch in `old_string`, requiring a re-read of the file and full block replacement.
- Graders run and results (PASS/FAIL): None.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Implement automated end-to-end tests to verify the AI's behavior with duplicate task creation scenarios.
