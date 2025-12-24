# Python To-Do List CLI

This is a simple but powerful command-line interface (CLI) application for managing your to-do list.

## Features

- Add, update, remove, and list tasks.
- Mark tasks as complete or to-do.
- Clean, user-friendly interface powered by `rich`.

## Prerequisites

- Python 3.7+

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

With the virtual environment activated, run the application with:

```bash
python main.py
```

## Available Commands

- `list`: Show all tasks
- `add <title> <description>`: Add a new task
- `update <id> <title> <description>`: Update a task
- `complete <id>`: Toggle a task's status
- `remove <id>`: Remove a task
- `help`: Show the help menu
- `exit`: Exit the application
