---
id: 39
title: Strictly Enforce Duplicate Task Prevention
stage: green
date: 2025-12-27
surface: agent
model: gemini-cli
feature: 002-todo-web-app
branch: master
user: {{USER}}
command: /sp.implement
labels: ["backend", "python", "bugfix", "validation"]
links:
  spec: specs/002-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
- backend/src/routes/chat.py
tests:
- (none)
---

## Prompt

/sp.implement Act as a Senior Backend Developer.

**Objective:** Fix the Duplicate Task bug in `backend/src/routes/chat.py`.

**Action:**
Update the `add_my_task` tool function to strictly check for existing tasks before creating a new one.

**Revised Logic:**
1. Fetch all tasks for the `current_user_id` using `get_tasks(db, current_user_id)`.
2. Clean the input `title` (remove extra spaces and convert to lowercase).
3. Compare the new title with all existing task titles.
4. If a match is found, DO NOT call `create_task`. Instead, return the string: "Error: A task with this exact title already exists."
5. If no match is found, proceed with `create_task` and return: "Success: Task added."

**AI Instruction:**
Tell the Gemini model in the system prompt area that if the tool returns "Error: A task with this exact title already exists", it must inform the user that the task is already in the list.

**Output:** Confirm when the duplicate prevention logic is strictly enforced.

## Response snapshot

I have updated `backend/src/routes/chat.py` to strictly enforce duplicate task prevention and updated the system instruction for the Gemini model.

## Outcome

- ✅ Impact: Duplicate tasks are now strictly prevented in the `add_my_task` function, and the Gemini model is instructed to inform the user about existing tasks.
- 🧪 Tests: No new tests were added.
- 📁 Files: `backend/src/routes/chat.py` was modified.
- 🔁 Next prompts: none
- 🧠 Reflection: This fix improves data integrity and user experience by preventing redundant task entries and providing clear feedback.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment: none
