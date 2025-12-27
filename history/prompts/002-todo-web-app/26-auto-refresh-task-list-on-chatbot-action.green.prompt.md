---
id: 26
title: Auto-Refresh Task List on Chatbot Action
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: /sp.implement Refresh the Task List automatically when the Chatbot adds a new task (without reloading the page).
labels: [implementation, frontend, event-handling, ui-refresh]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/ChatWidget.tsx
  - frontend/src/app/dashboard/page.tsx
tests: []
---

## Prompt

```text
/sp.implement Act as a Senior Frontend Developer.

**Objective:** Refresh the Task List automatically when the Chatbot adds a new task (without reloading the page).

**Strategy:** Use a custom Window Event (`taskUpdated`) to communicate between the ChatWidget and the Dashboard.

**Action 1: Update `frontend/src/components/ChatWidget.tsx` (The Sender)**
1.  Locate the `handleSendMessage` function.
2.  Immediately after the `axios.post` call returns successfully (and before setting the input to empty), dispatch the event:
    ```javascript
    // Notify the app that tasks have changed
    window.dispatchEvent(new Event('taskUpdated'));
    ```

**Action 2: Update `frontend/src/app/dashboard/page.tsx` (The Receiver)**
(Or whichever file contains the `fetchTasks` function and displays the list).
1.  Locate the `useEffect` hook that calls `fetchTasks()` on initial load.
2.  Add an event listener to listen for the 'taskUpdated' event.
    ```javascript
    useEffect(() => {
        fetchTasks(); // Initial load

        // Listen for updates from ChatWidget
        const handleTaskUpdate = () => {
            console.log("🔔 Chatbot triggered task refresh!");
            fetchTasks();
        };

        window.addEventListener('taskUpdated', handleTaskUpdate);

        // Cleanup on unmount
        return () => window.removeEventListener('taskUpdated', handleTaskUpdate);
    }, []);
    ```

**Output:**
Confirm when the event dispatch and listener are implemented.
```

## Response snapshot

```text
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/frontend/src/components/ChatWidget.tsx (1 replacements).
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/frontend/src/app/dashboard/page.tsx (1 replacements).
```

## Outcome

- ✅ Impact: Successfully implemented automatic refreshing of the task list. The `ChatWidget` now dispatches a custom `taskUpdated` event after a successful task-related action (e.g., adding a task), and the `dashboard/page.tsx` listens for this event, triggering a `fetchTasks()` call to update the UI without requiring a full page reload.
- 🧪 Tests: No new tests were added. Verification involves adding/deleting/updating tasks via the chat widget and observing the task list on the dashboard update in real-time.
- 📁 Files: Modified `frontend/src/components/ChatWidget.tsx` and `frontend/src/app/dashboard/page.tsx`.
- 🔁 Next prompts: The task list refresh mechanism is now in place, improving user experience by providing immediate feedback on chatbot actions. Further steps could involve more granular event handling or a more centralized state management solution.
- 🧠 Reflection: Using custom `Window` events provides a simple and effective way for loosely coupled components to communicate updates across the application, especially in scenarios where a full-fledged state management library might be overkill.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
