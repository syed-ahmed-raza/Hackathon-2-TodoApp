---
id: 22
title: Improve Chat UI with Markdown Rendering and Better AI Instructions
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: /sp.implement Improve the Chat UI to look modern, professional, and formatted using Markdown and Emojis.
labels: [implementation, frontend, backend, ui/ux, markdown, emojis, gemini]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/routes/chat.py
  - frontend/src/components/ChatWidget.tsx
  - frontend/package.json
  - frontend/package-lock.json
tests: []
---

## Prompt

```text
/sp.implement Act as a Senior Full Stack Developer.

**Objective:** Improve the Chat UI to look modern, professional, and formatted using Markdown and Emojis.

**Action 1: Update `backend/src/routes/chat.py` (Better AI Instructions)**
1.  Inside `chat_agent`, locate the system instruction or where you define the model.
2.  Add a system instruction or prepend to the user message: 
    "You are a helpful and professional AI assistant for a Todo App. When listing tasks, ALWAYS use Markdown bullet points. Use emojis for status (e.g., ✅ for Completed, ⏳ for Pending). Keep the tone encouraging and modern. Format the output cleanly."

**Action 2: Update `frontend/src/components/ChatWidget.tsx` (Render Markdown)**
1.  Import `ReactMarkdown` at the top: `import ReactMarkdown from 'react-markdown';`
2.  Locate where the message content is displayed (inside the `map` function for messages).
3.  Replace the plain `{msg.content}` with:
    ```tsx
    <div className="prose prose-sm max-w-none text-white">
        <ReactMarkdown
            components={{
                ul: ({node, ...props}) => <ul className="list-disc pl-4 space-y-1" {...props} />,
                li: ({node, ...props}) => <li className="marker:text-yellow-300" {...props} />,
                strong: ({node, ...props}) => <span className="font-bold text-yellow-300" {...props} />
            }}
        >
            {msg.content}
        </ReactMarkdown>
    </div>
    ```
    *(Note: Ensure the text color contrasts well with your purple chat bubble background).*

**Output:**
Confirm when backend instructions are improved and frontend is using ReactMarkdown.
```

## Response snapshot

```text
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/backend/src/routes/chat.py (1 replacements).
Successfully installed react-markdown.
Successfully modified file: D:\My Work/Coding/Governor Course/Q4/hackathon 2 todo list/frontend/src/components/ChatWidget.tsx (1 replacements).
```

## Outcome

- ✅ Impact: Successfully improved the Chat UI to be more modern, professional, and formatted. The backend now provides AI instructions to guide Gemini in using Markdown and emojis for task listings, and the frontend renders this content beautifully using `ReactMarkdown` with custom Tailwind CSS styling.
- 🧪 Tests: No explicit tests were added. Verification would involve running the application and interacting with the chat widget, confirming that AI responses are markdown-formatted with emojis and display correctly.
- 📁 Files: Modified `backend/src/routes/chat.py` and `frontend/src/components/ChatWidget.tsx`. Also updated `frontend/package.json` and `frontend/package-lock.json` due to `react-markdown` installation.
- 🔁 Next prompts: The chat UI is now significantly enhanced. Further steps could include more advanced theming, user personalization options, or additional AI capabilities.
- 🧠 Reflection: This task demonstrated a full-stack approach to UI improvement, coordinating changes between backend AI instructions and frontend rendering. The use of `ReactMarkdown` with custom components allows for fine-grained control over the rendered output's appearance.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
