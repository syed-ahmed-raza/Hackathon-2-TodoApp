"""
This module contains the complete To-Do List application in a single file.
It includes the data model, business logic, and user interface.
"""
import enum
from dataclasses import dataclass, field
from typing import List, Optional

from rich.console import Console
from rich.table import Table

# 1. Data Model
# ==============================================================================

class TaskStatus(enum.Enum):
    """Enumeration for the status of a task."""
    TODO = "To-Do"
    DONE = "Done"


@dataclass
class Task:
    """
    Represents a single task in the to-do list.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): A detailed description of the task.
        status (TaskStatus): The current status of the task.
    """
    id: int
    title: str
    description: str
    status: TaskStatus = field(default=TaskStatus.TODO)


# 2. Business Logic
# ==============================================================================

class TaskNotFoundError(Exception):
    """Exception raised when a task is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID '{task_id}' not found.")


class TodoService:
    """
    Manages tasks and the core business logic of the application.
    """
    def __init__(self):
        """Initializes the TodoService with an in-memory task list."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: str) -> Task:
        """
        Adds a new task to the list.

        Args:
            title: The title of the task.
            description: The description of the task.

        Returns:
            The newly created Task object.
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all Task objects.
        """
        return self._tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Finds a single task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task object if found, otherwise None.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str, description: str) -> Task:
        """
        Updates a task's title and description.

        Args:
            task_id: The ID of the task to update.
            title: The new title for the task.
            description: The new description for the task.

        Returns:
            The updated Task object.
        
        Raises:
            TaskNotFoundError: If the task with the given ID is not found.
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        task.title = title
        task.description = description
        return task

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggles a task's status between TODO and DONE.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated Task object.

        Raises:
            TaskNotFoundError: If the task with the given ID is not found.
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        
        task.status = TaskStatus.DONE if task.status == TaskStatus.TODO else TaskStatus.TODO
        return task

    def remove_task(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was removed successfully.

        Raises:
            TaskNotFoundError: If the task with the given ID is not found.
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        self._tasks.remove(task)
        return True

# 3. UI Logic
# ==============================================================================

class TodoApp:
    """
    The command-line interface for interacting with the To-Do application.
    """

    def __init__(self, service: TodoService):
        """
        Initializes the CLI with a TodoService instance.

        Args:
            service: The service layer for managing tasks.
        """
        self._service = service
        self._console = Console()

    def _display_tasks(self):
        """Displays all tasks in a formatted table."""
        tasks = self._service.get_all_tasks()
        table = Table(title="To-Do List")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="yellow")
        table.add_column("Description", justify="left")
        table.add_column("Status", style="magenta")

        if not tasks:
            self._console.print("[bold red]No tasks found.[/bold red]")
            return

        for task in tasks:
            status_color = "green" if task.status.value == "Done" else "red"
            table.add_row(
                str(task.id),
                task.title,
                task.description,
                f"[{status_color}]{task.status.value}[/{status_color}]"
            )
        
        self._console.print(table)

    def _show_help(self):
        """Displays the help menu."""
        self._console.print("\n[bold]Available Commands:[/bold]")
        self._console.print("  [cyan]list[/cyan]                            - Show all tasks")
        self._console.print("  [cyan]add <title> <desc>[/cyan]          - Add a new task")
        self._console.print("  [cyan]update <id> <title> <desc>[/cyan]   - Update a task")
        self._console.print("  [cyan]complete <id>[/cyan]                 - Toggle a task's status")
        self._console.print("  [cyan]remove <id>[/cyan]                   - Remove a task")
        self._console.print("  [cyan]help[/cyan]                           - Show this help menu")
        self._console.print("  [cyan]exit[/cyan]                           - Exit the application\n")


    def run(self):
        """
        Main loop for the CLI, parsing user input and executing commands.
        """
        self._console.print("[bold green]Welcome to the To-Do List App![/bold green]")
        self._show_help()

        while True:
            try:
                command_str = self._console.input("[bold cyan]> [/bold cyan]").strip()
                if not command_str:
                    continue
                
                command = command_str.split()
                action = command[0].lower()

                if action == "exit":
                    self._console.print("[bold]Goodbye![/bold]")
                    break
                elif action == "help":
                    self._show_help()
                elif action == "list":
                    self._display_tasks()
                elif action == "add":
                    parts = command_str.split(maxsplit=2)
                    if len(parts) < 3:
                        self._console.print("[bold red]Usage: add <title> <description>[/bold red]")
                        continue
                    _, title, description = parts
                    task = self._service.add_task(title, description)
                    self._console.print(f"[green]Added task {task.id}: '{task.title}'[/green]")
                    self._display_tasks()
                elif action == "update":
                    parts = command_str.split(maxsplit=3)
                    if len(parts) < 4:
                        self._console.print("[bold red]Usage: update <id> <title> <description>[/bold red]")
                        continue
                    _, task_id_str, title, description = parts
                    task_id = int(task_id_str)
                    self._service.update_task(task_id, title, description)
                    self._console.print(f"[green]Updated task {task_id}[/green]")
                    self._display_tasks()
                elif action == "complete":
                    if len(command) < 2:
                        self._console.print("[bold red]Usage: complete <id>[/bold red]")
                        continue
                    task_id = int(command[1])
                    task = self._service.toggle_complete(task_id)
                    self._console.print(f"[green]Task {task_id} status changed to {task.status.value}[/green]")
                    self._display_tasks()
                elif action == "remove":
                    if len(command) < 2:
                        self._console.print("[bold red]Usage: remove <id>[/bold red]")
                        continue
                    task_id = int(command[1])
                    self._service.remove_task(task_id)
                    self._console.print(f"[green]Removed task {task_id}[/green]")
                    self._display_tasks()
                else:
                    self._console.print(f"[bold red]Unknown command: '{action}'[/bold red]")
                    self._show_help()

            except ValueError:
                self._console.print("[bold red]Invalid input. Please enter a valid task ID.[/bold red]")
            except TaskNotFoundError as e:
                self._console.print(f"[bold red]Error: {e}[/bold red]")
            except Exception as e:
                self._console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

# 4. Application Entry Point
# ==============================================================================

def main():
    """
    Initializes the application components and starts the command-line interface.
    """
    service = TodoService()
    app = TodoApp(service)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nApplication exited.")


if __name__ == "__main__":
    main()