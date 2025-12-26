# Tasks: Todo Web Application

**Input**: Design documents from `specs/002-todo-web-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure.

- [X] T001 Create monorepo directory structure: `backend/` and `frontend/` directories.
- [ ] T002 [P] Create a `.gitignore` file at the repository root with common Python and Node.js ignores.

---

## Phase 2: Foundational (Backend & Frontend Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

### Backend
- [ ] T003 Initialize the Python project in `backend/` and create a `requirements.txt` with FastAPI, SQLModel, uvicorn, passlib, python-jose.
- [ ] T004 Implement database models for `User` and `Task` in `backend/src/models.py` based on `data-model.md`.
- [ ] T005 Implement the database connection logic in `backend/src/database.py` to connect to a SQLite database.
- [ ] T006 Implement the main FastAPI application entrypoint in `backend/src/main.py`, including CORS middleware.

### Frontend
- [ ] T007 [P] Initialize a new Next.js application in the `frontend/` directory.
- [ ] T008 [P] Implement a typed API client service in `frontend/src/lib/api.ts` to handle requests to the backend.

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Allow users to sign up, log in, and log out.

**Independent Test**: A user can create an account, log out, and log back in to receive a valid JWT. The frontend routes are protected.

### Implementation for User Story 1

- [ ] T009 [US1] Implement password hashing and JWT generation/verification logic in `backend/src/auth.py`.
- [ ] T010 [US1] Implement the `/auth/signup` and `/auth/login` API endpoints in a new `backend/src/routes/auth.py` router.
- [ ] T011 [US1] Integrate the auth router into the main FastAPI app in `backend/src/main.py`.
- [ ] T012 [P] [US1] Create Signup and Login pages/components in `frontend/src/app/(auth)/`.
- [ ] T013 [US1] Implement state management and logic for user authentication (signup, login, logout) on the frontend.
- [ ] T014 [US1] Protect the main dashboard page, redirecting unauthenticated users to the login page.

---

## Phase 4: User Story 2 - Task Creation and Viewing (Priority: P2)

**Goal**: Allow logged-in users to create tasks and view their task list.

**Independent Test**: A logged-in user can add a new task via the UI, and it appears in their task list.

### Implementation for User Story 2

- [ ] T015 [US2] Create a new `backend/src/routes/tasks.py` router.
- [ ] T016 [US2] Implement the `GET /tasks` and `POST /tasks` endpoints in `backend/src/routes/tasks.py`. These must be protected and operate only on the authenticated user's data.
- [ ] T017 [US2] Integrate the tasks router into the main FastAPI app in `backend/src/main.py`.
- [ ] T018 [P] [US2] Create the main dashboard UI in `frontend/src/app/dashboard/page.tsx` to display a list of tasks.
- [ ] T019 [US2] Implement the "Add Task" form component.
- [ ] T020 [US2] Connect the frontend dashboard to the backend API to fetch and display the user's tasks, and to create new tasks.

---

## Phase 5: User Story 3 - Task Management (Priority: P3)

**Goal**: Allow users to update, complete, and delete their tasks.

**Independent Test**: A user can successfully edit a task title, toggle its completion status, and delete it from the UI.

### Implementation for User Story 3

- [ ] T021 [US3] Implement the `PUT /tasks/{id}`, `DELETE /tasks/{id}`, and `PATCH /tasks/{id}/complete` endpoints in `backend/src/routes/tasks.py`.
- [ ] T022 [P] [US3] Add UI elements (buttons, forms) to the dashboard for editing, deleting, and toggling task completion.
- [ ] T023 [US3] Connect the new UI elements to their corresponding backend API endpoints.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T024 [P] Add global error handling and user feedback (e.g., loading spinners, toast notifications) to the frontend.
- [ ] T025 [P] Write or update the main `README.md` with instructions from `quickstart.md`.
- [ ] T026 [P] Add basic unit tests for the backend authentication logic in `backend/tests/`.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (Foundational)** depends on Phase 1. Backend and Frontend tasks within Phase 2 can run in parallel.
- **User Stories (Phase 3+)** depend on Phase 2.
- **US1 (Auth)** is the highest priority and blocks other user stories as they require an authenticated user.
- **US2 (Create/View)** depends on US1.
- **US3 (Manage)** depends on US2.
