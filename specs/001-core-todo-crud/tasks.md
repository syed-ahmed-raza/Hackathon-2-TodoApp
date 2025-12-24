# Tasks: Core To-Do List CRUD

**Input**: `specs/001-core-todo-crud/plan.md`

## Phase 1: Setup

**Purpose**: Initialize the Python project structure and dependencies.

- [x] T001 Create the directory structure: `src/models`, `src/services`, `src/ui`.
- [x] T002 Create an empty `requirements.txt` file for project dependencies.
- [x] T003 Add `rich` to `requirements.txt`.
- [x] T004 Create an empty file named `CLAUDE.md` at the root.

---

## Phase 2: User Story 1 - Core Task Management

**Goal**: As a user, I can add, view, update, and delete tasks through the command-line interface.

**Independent Test**:
1. Run `python main.py`.
2. Add a new task.
3. List tasks and verify the new task is present.
4. Update the task.
5. List tasks and verify the task is updated.
6. Mark the task as complete.
7. List tasks and verify the status has changed.
8. Delete the task.
9. List tasks and verify the task is gone.

### Implementation for User Story 1

- [x] T005 [US1] Implement the `Task` dataclass and `TaskStatus` enum in `src/models/task.py`.
- [x] T006 [US1] Implement the `TodoService` class with an in-memory list in `src/services/todo_service.py`.
- [x] T007 [US1] Implement the `add_task` and `get_all_tasks` methods in `src/services/todo_service.py`.
- [x] T008 [US1] Implement the `update_task`, `remove_task`, and `toggle_complete` methods in `src/services/todo_service.py`, including error handling for non-existent tasks.
- [x] T009 [US1] Implement the basic `CLI` class structure in `src/ui/cli.py`, accepting the `TodoService` in its constructor.
- [x] T010 [US1] Implement the main `run` loop in `src/ui/cli.py` to parse user commands (add, list, update, complete, remove, exit).
- [x] T011 [US1] Implement the `_display_tasks` method in `src/ui/cli.py` using the `rich` library to show tasks in a table.
- [x] T012 [US1] Create the `main.py` entry point to initialize `TodoService` and `CLI`, and call the `run` method.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Improve documentation and finalize the application for initial release.

- [x] T013 Create a `README.md` with instructions on how to set up and run the project.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (User Story 1)** depends on Phase 1. All tasks within Phase 2 can be worked on sequentially as they build upon each other.
- **Phase 3 (Polish)** can be done after Phase 2 is complete.
