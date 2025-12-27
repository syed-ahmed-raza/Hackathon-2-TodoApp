---
id: 25
title: Fix 429 Resource Exhausted Error and Clean Up Chat Output
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: "/sp.implement Fix \"429 Resource Exhausted\" error and clean up Chat output (remove IDs)."
labels: [implementation, backend, bugfix, gemini, model-name, output-formatting]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/routes/chat.py
tests: []
---

## Prompt

```text
/sp.implement Act as a Senior Python Developer.

**Objective:** Fix "429 Resource Exhausted" error and clean up Chat output (remove IDs).

**Diagnosis:**
1. The model `gemini-2.5-flash` has a very low daily limit (20 requests). We must switch to `gemini-2.0-flash`.
2. The `get_my_tasks` tool is likely returning raw data including IDs. We need to format it to return only relevant info.

**Action: Update `backend/src/routes/chat.py`**

1.  **Update Tool Function (`get_my_tasks`):**
    Rewrite the function inside `chat_agent` to return a clean, human-friendly string.
    ```python
    def get_my_tasks():
        """Gets the user's tasks in a simple text format."""
        tasks = get_tasks(db, current_user_id)
        if not tasks:
            return "You have no tasks currently."
        # Returns: "- Task Name (Status)"
        return "\n".join([f"- {t.title} ({'✅ Completed' if t.completed else '⏳ Pending'})") for t in tasks])
    ```

2.  **Update Model Initialization:**
    Change the model name to `"gemini-2.0-flash"`.
    ```python
    # Use gemini-2.0-flash which typically has higher limits than 2.5-flash
    model = genai.GenerativeModel("gemini-2.0-flash", tools=[add_my_task, get_my_tasks, delete_my_task])
    ```

**Output:**
Confirm when the model is switched to 2.0-flash and the tool output is cleaned.
```

## Response snapshot

```text
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/backend/src/routes/chat.py (1 replacements).
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/backend/src/routes/chat.py (1 replacements).
```

## Outcome

- ✅ Impact: Successfully addressed the "429 Resource Exhausted" error by switching the Gemini model from `"gemini-flash-latest"` (which was effectively `"gemini-2.5-flash"`) to `"gemini-2.0-flash"`, which has higher quota limits. Additionally, the `get_my_tasks` function was refined to return a clean, human-friendly string without internal task IDs, improving the readability of AI responses.
- 🧪 Tests: No new tests were added. Verification would involve interacting with the chat widget and confirming both that the API calls succeed without quota errors and that task listings are formatted as expected.
- 📁 Files: Modified `backend/src/routes/chat.py`.
- 🔁 Next prompts: The chat functionality should now be more stable and provide cleaner output. Further improvements could involve more dynamic tool outputs or additional error handling.
- 🧠 Reflection: This task highlights the importance of understanding model quotas and output formatting when integrating AI assistants. Choosing the right model and shaping its output for a better user experience are key aspects of AI development.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

```