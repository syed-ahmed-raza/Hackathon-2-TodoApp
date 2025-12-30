# Tasks: Cloud-Native Deployment

**Input**: Design documents from `/specs/003-cloud-native-deployment/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Containerization Setup

**Purpose**: Create Docker artifacts for containerizing the frontend and backend services.

- [ ] T001 [P] [US1] Create Dockerfile for the backend service in `backend/Dockerfile`.
- [ ] T002 [P] [US1] Create Dockerfile for the frontend service in `frontend/Dockerfile`.
- [ ] T003 [P] [US1] Create .dockerignore file for the backend service in `backend/.dockerignore`.
- [ ] T004 [P] [US1] Create .dockerignore file for the frontend service in `frontend/.dockerignore`.

---

## Phase 2: Image Building

**Purpose**: Build container images and load them into the Minikube environment.

- [ ] T005 [US1] Configure local environment to use Minikube's Docker daemon.
- [ ] T006 [US1] Build the backend Docker image with tag `todo-backend:v1`.
- [ ] T007 [US1] Build the frontend Docker image with tag `todo-frontend:v1`.

---

## Phase 3: Helm Chart Implementation

**Purpose**: Develop a Helm chart to manage the deployment of the application services.

- [ ] T008 [US2] Create a new directory `charts/`.
- [ ] T009 [US2] Initialize a new Helm chart named `todo-chatbot` inside the `charts/` directory.
- [ ] T010 [US2] Configure `charts/todo-chatbot/values.yaml` with image repositories, tags, and replica counts.
- [ ] T011 [US2] Create a Kubernetes Deployment template for the backend in `charts/todo-chatbot/templates/backend-deployment.yaml`.
- [ ] T012 [US2] Create a Kubernetes Service template for the backend in `charts/todo-chatbot/templates/backend-service.yaml`.
- [ ] T013 [US2] Create a Kubernetes Deployment template for the frontend in `charts/todo-chatbot/templates/frontend-deployment.yaml`.
- [ ] T014 [US2] Create a Kubernetes Service template for the frontend in `charts/todo-chatbot/templates/frontend-service.yaml`.
- [ ] T015 [US2] Create a Kubernetes Secret template in `charts/todo-chatbot/templates/secrets.yaml` to manage `DATABASE_URL` and `GEMINI_API_KEY`.

---

## Phase 4: Deployment and Verification

**Purpose**: Deploy the application using Helm and verify its operation.

- [ ] T016 [US2] Deploy the application using the `helm install` command.
- [ ] T017 [US2] Verify the status of the deployed Pods using `kubectl get pods`.
- [ ] T018 [US2] Port-forward the frontend service to access the application from the browser.
- [ ] T_019 [US2] Test application functionality and connectivity between frontend and backend.

## Dependencies & Execution Order

- **Phase 1 (Containerization)**: Can start immediately. Tasks T001-T004 can be done in parallel.
- **Phase 2 (Image Building)**: Depends on Phase 1. Must be done sequentially (T005 -> T006 -> T007).
- **Phase 3 (Helm)**: Depends on Phase 1. Can be done in parallel with Phase 2. Tasks T010-T015 can be done in parallel after T009.
- **Phase 4 (Deployment)**: Depends on Phase 2 and 3. Must be done sequentially.
