# Quickstart for Todo Web Application

This guide provides instructions for setting up and running the frontend and backend services.

## Prerequisites

- Python 3.11+
- Node.js 20+
- `uv` (or `pip`) for Python package management
- `npm` or `yarn` for Node.js package management

## Backend Setup (FastAPI)

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

## Frontend Setup (Next.js)

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
