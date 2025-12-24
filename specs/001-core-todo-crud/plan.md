# Plan: Python To-Do List CLI

**Feature:** `speckit` - Core To-Do List Application
**Version:** 1.0.0

## 1. Architectural Goals

This plan outlines a modular Python application with a clear separation of concerns, dividing the application into three distinct layers:

-   **Data Layer (`/src/models`):** Contains the data structures (dataclasses) that represent the application's entities.
-   **Logic Layer (`/src/services`):** Implements the business logic and manages the application's state.
-   **Presentation Layer (`/src/ui`):** Handles all user interaction, command parsing, and output rendering.

This design ensures that the application is easy to maintain, extend, and test.

## 2. Folder Structure

The project will be organized as follows to enforce the separation of concerns.

```
/
|-- src/
|   |-- models/
|   |   |-- __init__.py
|   |   `-- task.py         # Contains the Task dataclass
|   |-- services/
|   |   |-- __init__.py
|   |   `-- todo_service.py # Contains the TodoService class
|   |-- ui/
|   |   |-- __init__.py
|   |   `-- cli.py          # Contains the CLI class for user interaction
|   `-- __init__.py
|-- main.py                 # Application entry point
|-- requirements.txt        # Project dependencies (e.g., rich)
`-- tests/
    |-- test_todo_service.py
    `-- test_cli.py
```

## 3. Component Design

### 3.1. Data Model (`/src/models/task.py`)

The `Task` model will be a `dataclass` to hold task information. A status `Enum` will be used to represent the state of a task.

```python
# src/models/task.py
import enum
from dataclasses import dataclass, field

class TaskStatus(enum.Enum):
    TODO = "To-Do"
    DONE = "Done"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus = field(default=TaskStatus.TODO)
```

### 3.2. Business Logic (`/src/services/todo_service.py`)

The `TodoService` class will manage an in-memory list of `Task` objects and contain all the business logic for manipulating tasks.

```python
# src/services/todo_service.py
from typing import List, Optional
from src.models.task import Task, TaskStatus

class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: str) -> Task:
        """Adds a new task."""
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks."""
        return self._tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """Finds a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str, description: str) -> Optional[Task]:
        """Updates a task's title and description."""
        task = self.get_task(task_id)
        if task:
            task.title = title
            task.description = description
        return task

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggles a task's status between TODO and DONE."""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.DONE if task.status == TaskStatus.TODO else TaskStatus.TODO
        return task

    def remove_task(self, task_id: int) -> bool:
        """Removes a task by its ID."""
        task = self.get_task(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False
```

### 3.3. User Interface (`/src/ui/cli.py`)

The `CLI` class will handle all command-line interactions. It will use the `rich` library to create a more user-friendly and visually appealing interface.

```python
# src/ui/cli.py
from src.services.todo_service import TodoService
# Rich will be used for printing tables and formatted text.
from rich.console import Console
from rich.table import Table

class CLI:
    def __init__(self, service: TodoService):
        self._service = service
        self._console = Console()

    def run(self):
        """Main loop for the CLI."""
        # Implementation for the input loop, command parsing, and calling service methods.
        # This will include commands for: add, list, update, complete, remove, exit.
        pass

    def _display_tasks(self):
        """Displays all tasks in a formatted table."""
        table = Table(title="To-Do List")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Status", style="magenta")

        for task in self._service.get_all_tasks():
            table.add_row(str(task.id), task.title, task.status.value)
        
        self._console.print(table)

```

### 3.4. Entry Point (`main.py`)

The `main.py` file will initialize the application components and start the CLI.

```python
# main.py
from src.services.todo_service import TodoService
from src.ui.cli import CLI

def main():
    service = TodoService()
    cli = CLI(service)
    cli.run()

if __name__ == "__main__":
    main()
```

## 4. Data Flow

The data will flow through the application in a unidirectional manner:

1.  **User Input:** The user enters a command in the terminal (e.g., `add "My new task"`).
2.  **CLI Processing:** The `CLI` class receives the input, parses it to identify the command and its arguments.
3.  **Service Call:** The `CLI` calls the appropriate method on the `TodoService` instance (e.g., `_service.add_task(...)`).
4.  **State Mutation:** The `TodoService` performs the business logic, mutating the in-memory list of tasks.
5.  **Response:** The `TodoService` returns a result (e.g., the newly created `Task` object or a boolean status).
6.  **Display:** The `CLI` receives the response and uses its `_display_tasks` or another rendering method to show the updated state to the user.

## 5. Constitution Check

-   **Modularity:** The proposed architecture enforces modularity by design.
-   **Clarity:** The separation of concerns makes the code's purpose clear.
-   **Testability:** `TodoService` can be tested independently of the UI.
-   **Extensibility:** New features can be added by extending the service and adding corresponding commands in the CLI without major refactoring.

## 6. Research and Clarifications

-   **UI Library:** The `rich` library is chosen for its ability to create beautiful and informative CLI outputs with minimal effort. It improves the user experience over standard `print` statements. This is a standard choice for modern Python CLI applications and requires no further research.

## 7. Quickstart

1.  **Setup:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Run:**
    ```bash
    python main.py
    ```
