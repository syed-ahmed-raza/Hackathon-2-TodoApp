---
id: 6
title: Configure Frontend for Live Render Backend URL
stage: green
date: 2025-12-26
surface: agent
model: gemini-1.5-pro
feature: 002-todo-web-app
branch: main
user: user
command: /sp.implement Configure the Frontend to use the Live Render Backend URL.
labels: [implementation, frontend, api-config]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests: []
---

## Prompt

```text
/sp.implement Act as a Deployment Engineer.

**Objective:** Configure the Frontend to use the Live Render Backend URL.

**Action:**
Update `frontend/src/lib/api.ts`:
1.  Locate the `API_BASE_URL` definition.
2.  Update it to check `process.env.NEXT_PUBLIC_API_URL` first.
3.  The logic should be: `const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';`
4.  Ensure there are NO trailing slashes in the logic.

**Output:**
Provide the corrected code for `frontend/src/lib/api.ts`.
```

## Response snapshot

```text
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('Token:', token);
  if (token && !config.url?.includes('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const signup = (data: any) => {
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);

    return apiClient.post('/auth/signup', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
};

export const login = (data: any) => {
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);

    return apiClient.post('/auth/login', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
};

export const getTasks = () => apiClient.get('/tasks');
export const addTask = (data: any) => apiClient.post('/tasks', data);
export const updateTask = (id: number, data: any) => apiClient.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => apiClient.delete(`/tasks/${id}`);
```

## Outcome

- ✅ Impact: Successfully updated API configuration for the frontend to use a dynamic backend URL based on environment variables, with a fallback to localhost.
- 🧪 Tests: No new tests were added as this was a configuration change. Existing tests for API calls should continue to pass, now targeting the correct environment.
- 📁 Files: Modified `frontend/src/lib/api.ts`.
- 🔁 Next prompts: None for this specific task. The user can now proceed with deployment or further development, ensuring the `NEXT_PUBLIC_API_URL` environment variable is set appropriately for their deployment environment.
- 🧠 Reflection: The previous attempt to create a PHR using a bash script failed because `bash` was not available in the execution environment. This highlights the need for agent-native tools or careful environment checks before using shell commands that rely on specific shell interpreters. The agent successfully adapted by manually constructing and writing the PHR file.

## Evaluation notes (flywheel)

- Failure modes observed: `bash` command not found when attempting to create PHR via shell script.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
