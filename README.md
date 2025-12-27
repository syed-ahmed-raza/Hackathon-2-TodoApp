# Hackathon II: Full-Stack To-Do Application

This project is a full-stack to-do list application built for Phase II of the hackathon. It features a Next.js frontend, a FastAPI backend, and a PostgreSQL database.

## Architecture

This project follows a monorepo structure:

-   `/frontend`: Contains the Next.js 16+ (App Router) and Tailwind CSS client-side application.
-   `/backend`: Contains the Python FastAPI server, using SQLModel as the ORM.

## Tech Stack

-   **Frontend:** Next.js, React, Tailwind CSS
-   **Backend:** Python, FastAPI, SQLModel
-   **Database:** Neon Serverless Postgres (production), SQLite (local development)
-   **Development Process:** Spec-Driven Development (SDD)

## Getting Started

To get the application up and running, follow these steps:

### Prerequisites

-   Python 3.11+
-   Node.js 20+
-   `uv` (or `pip`) for Python package management
-   `npm` or `yarn` for Node.js package management

### 1. Clone the repository

```bash
git clone <repository_url>
cd hackathon-2-todo-list # Replace with your repository name
```

### 2. Backend Setup (FastAPI)

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```

4.  Run the development server:
    ```bash
    uvicorn src.main:app --reload
    ```

The backend API will be available at `http://127.0.0.1:8000`.

### 3. Frontend Setup (Next.js)

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

The frontend application will be available at `http://localhost:3000`.