---
id: 44
title: Fix AI "Hallucination Bug" via System Instruction
stage: green
date: 2025-12-27
surface: agent
model: gemini
feature: 002-todo-web-app
branch: master
user: syed-ahmed-raza
command: /sp.implement
labels: ["backend", "bugfix", "ai", "system-instruction", "tool-usage"]
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
/sp.implement Act as a Senior AI Engineer.

**Objective:** Fix the "Hallucination Bug" where AI says it added a task but doesn't actually call the tool.

**Action:**
Update the `system_instruction` in `backend/src/routes/chat.py` to strictly enforce tool usage.

**New System Instruction:**
```python
system_instruction = """You are a smart, friendly, and professional AI Assistant for a Todo App.

**CRITICAL RULE:**
- You **cannot** perform actions just by replying with text. 
- You **MUST** call the provided tools (`add_my_task`, `delete_my_task`, `get_my_tasks`) to actually change the database.
- Do not confirm an action unless you have called the tool.

**Guidelines:**
1. **Language Adaptability:**
   - English -> Professional English.
   - Roman Urdu/Hindi -> Reply in Roman Urdu (e.g., "Ji zaroor, task add kar diya ✅").
2. **Personality:** Be polite and use emojis (✅, 🗑️, 📝).
3. **Task Operations:**
   - **Adding:** Call `add_my_task` first. Then say: "Done! ✅ I've added '[Task Name]'."
   - **Deleting:** Call `delete_my_task` with the NAME. Then say: "Deleted '[Task Name]' 🗑️."
   - **Listing:** Call `get_my_tasks`.

**Tools:**
- Use `add_my_task`, `delete_my_task`, and `get_my_tasks`.
- Never ask for an ID; handle deletions by name."""
```

## Response snapshot

The agent successfully updated the `system_instruction` variable in `backend/src/routes/chat.py` with stricter rules, aiming to resolve the AI "Hallucination Bug." The new instruction explicitly mandates tool usage for actions, preventing the AI from confirming actions without actual database changes.

## Outcome

- ✅ Impact: The AI assistant is now strictly guided to use its tools for task management operations, which should eliminate instances of "hallucination" and ensure that confirmed actions reflect actual changes in the database.
- 🧪 Tests: Manual verification of the `backend/src/routes/chat.py` file content confirmed the successful update of the `system_instruction` variable.
- 📁 Files: Modified `backend/src/routes/chat.py`.
- 🔁 Next prompts: The user can now proceed with further development or ask for new features.
- 🧠 Reflection: Explicitly defining tool usage rules in the system instruction is a critical step in controlling AI agent behavior and ensuring reliability in function-calling scenarios.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): None.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Integrate logging for tool calls to monitor AI adherence to the new system instruction and identify any remaining "hallucination" patterns.
