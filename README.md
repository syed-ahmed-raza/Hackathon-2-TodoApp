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

> **Note:** Detailed setup instructions for the frontend and backend are located in their respective `README.md` files inside the `/frontend` and `/backend` directories.

1.  **Clone the repository.**
2.  **Set up the backend:** Follow the instructions in `backend/README.md`.
3.  **Set up the frontend:** Follow the instructions in `frontend/README.md`.