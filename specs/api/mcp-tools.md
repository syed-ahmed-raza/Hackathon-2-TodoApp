# MCP Tools Specification
The Backend will expose functions (Tools) for the OpenAI Agent:
1. `add_task(title, description)`
2. `list_tasks(status_filter)`
3. `delete_task(task_id)`
4. `complete_task(task_id)`
These tools must interact directly with the existing SQLModel database.
