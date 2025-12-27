---
id: 33
title: Implement Fallback for Chatbot Model
stage: green
date: 2025-12-27
surface: agent
model: gemini-cli
feature: 002-todo-web-app
branch: master
user: {{USER}}
command: /sp.implement
labels: ["chatbot", "backend", "python", "gemini"]
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

/sp.implement Act as a Senior Python Developer.

**Objective:** Implement a "Fallback Mechanism" for the Chatbot Model. It should try multiple Google Gemini models one by one until it finds a working one.

**Action: Update `backend/src/routes/chat.py`**
Replace the file content with this logic:

1.  **Imports:** Standard FastAPI, Pydantic, GenAI imports.
2.  **Tools:** Include `add_my_task`, `delete_my_task`, `get_my_tasks` (Clean output without IDs).
3.  **Model Logic (The Important Part):**
    -   Create a list of models: `["gemini-1.5-flash", "gemini-flash-latest", "gemini-2.0-flash-exp", "gemini-pro"]`.
    -   Use a `for` loop to try connecting to each model.
    -   If a model works (responds), return the text immediately.
    -   If a model fails (Exception), print the error and `continue` to the next model.
    -   If all fail, return a "System Busy" message.

**Code Reference:**
```python
    # ... inside chat_agent function ...
    models = ["gemini-1.5-flash", "gemini-flash-latest", "gemini-2.0-flash-exp", "gemini-pro"]
    
    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name, tools=[add_my_task, get_my_tasks, delete_my_task])
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request.message)
            return response.text
        except Exception:
            continue
            
    return "Error: All AI models are currently busy. Please try again later."
```

## Response snapshot

I have successfully implemented the fallback mechanism in `backend/src/routes/chat.py`.

## Outcome

- ✅ Impact: The chatbot is now more resilient to model failures.
- 🧪 Tests: No new tests were added.
- 📁 Files: `backend/src/routes/chat.py` was modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The implementation was straightforward and followed the user's request.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment: none
