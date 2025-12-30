# Technical Plan: 003-cloud-native-deployment

**Feature Branch**: `003-cloud-native-deployment`
**Created**: 2025-12-30
**Status**: Draft

## 1. Technical Context

This plan outlines the steps to containerize the "Todo Chatbot" application and deploy it to a local Kubernetes cluster (Minikube) using Helm. The goal is to create a reproducible, version-controlled deployment process that mirrors a cloud-native environment.

## 2. Plan

### Step 1: Containerization Setup

-   **Task 1.1: Create Backend Dockerfile**
    -   Create a file named `backend/Dockerfile`.
    -   Use the `python:3.11-slim` base image.
    -   Copy the `requirements.txt` and install dependencies.
    -   Copy the backend source code.
    -   Expose port `8000`.
    -   Set the command to run the FastAPI application using `uvicorn`.

-   **Task 1.2: Create Frontend Dockerfile**
    -   Create a file named `frontend/Dockerfile`.
    -   Use the `node:18-alpine` base image.
    -   Set the working directory.
    -   Copy `package.json` and `package-lock.json` and run `npm install`.
    -   Copy the frontend source code.
    -   Run `npm run build`.
    -   Expose port `3000`.
    -   Set the command to `npm start`.

-   **Task 1.3: Create `.dockerignore` files**
    -   Create `backend/.dockerignore` to exclude `__pycache__`, `.venv`, and other unnecessary files.
    -   Create `frontend/.dockerignore` to exclude `node_modules`, `.next`, and other build artifacts.

### Step 2: Build Images (Minikube Context)

-   **Task 2.1: Switch Docker to Minikube**
    -   Run the command to point the local Docker daemon to the Minikube internal Docker registry: `minikube docker-env`.

-   **Task 2.2: Build Backend Image**
    -   Navigate to the `backend` directory.
    -   Build the Docker image with the tag `todo-backend:v1`.

-   **Task 2.3: Build Frontend Image**
    -   Navigate to the `frontend` directory.
    -   Build the Docker image with the tag `todo-frontend:v1`.

### Step 3: Helm Chart Creation

-   **Task 3.1: Initialize Helm Chart**
    -   Create a `charts` directory in the root.
    -   Inside `charts`, initialize a new Helm chart named `todo-chatbot`.

-   **Task 3.2: Clean Up Chart**
    -   Remove the default templates and values that are not needed.

-   **Task 3.3: Define `values.yaml`**
    -   Structure `values.yaml` to configure:
        -   `backend.image.repository`, `backend.image.tag`, `backend.replicaCount`
        -   `frontend.image.repository`, `frontend.image.tag`, `frontend.replicaCount`
        -   `env.secrets` for `DATABASE_URL` and `GEMINI_API_KEY`.

### Step 4: Kubernetes Templates Implementation

-   **Task 4.1: Create Backend Manifests**
    -   Create `charts/todo-chatbot/templates/backend-deployment.yaml`.
    -   Create `charts/todo-chatbot/templates/backend-service.yaml` of type `ClusterIP`.

-   **Task 4.2: Create Frontend Manifests**
    -   Create `charts/todo-chatbot/templates/frontend-deployment.yaml`.
    -   Create `charts/todo-chatbot/templates/frontend-service.yaml` of type `NodePort`.

-   **Task 4.3: Implement Secret Handling**
    -   Create a `secrets.yaml` template to create a Kubernetes Secret from the values in `values.yaml`.
    -   Modify the Deployment templates to mount these secrets as environment variables.

### Step 5: Deployment & Verification

-   **Task 5.1: Deploy with Helm**
    -   Run `helm install` with a release name, pointing to the `todo-chatbot` chart.
    -   Pass the secret values using the `--set` flag or a separate values file.

-   **Task 5.2: Port-Forward Services**
    -   Use `kubectl port-forward` to access the `frontend-service` and `backend-service` on `localhost`.

-   **Task 5.3: Test Connectivity**
    -   Access the frontend in a browser.
    -   Verify that the frontend can communicate with the backend.
    -   Check logs to ensure the backend can connect to the database.

## 3. Constitution Check

-   **Spec-Driven Development**: This plan directly implements the approved specification.
-   **Code Quality**: Dockerfiles will be written following best practices.
-   **Technology Stack**: The plan uses the existing Python/FastAPI backend and Next.js frontend.
-   **Monorepo Architecture**: The plan respects the existing `frontend` and `backend` directory structure.
-   **Authentication**: Secrets are handled securely, which is a prerequisite for auth.