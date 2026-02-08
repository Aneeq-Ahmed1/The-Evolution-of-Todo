---
id: 0003
title: Todo Full-Stack Web App Tasks
stage: tasks
date: 2025-12-25
surface: feature
model: Claude Sonnet 4.5
feature: 001-fullstack-web-app
branch: 001-fullstack-web-app
user: Claude Code User
command: /sp.tasks
labels: [tasks, web-app, fullstack, implementation]
links:
  spec: ./spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-fullstack-web-app/tasks.md
    purpose: Development tasks for full-stack todo application
tests:
  - type: validation
    result: passed
    description: Tasks validated against plan and specification requirements
---

## Prompt

/sp.tasks

Project Phase: Phase II – Todo Full-Stack Web Application

Context:
- Phase I (In-memory Python CLI Todo App) is complete.
- Phase II specifications have been created under /specs using Spec-Kit.
- This is a monorepo using Spec-Kit + Claude Code.
- Frontend: Next.js (App Router)
- Backend: FastAPI + SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth with JWT

Goal:
Generate a clear, step-by-step implementation plan to move from specs to a working Phase II full-stack application.

Planning Requirements:
1. Break the work into logical milestones and ordered steps.
2. Clearly separate:
   - Backend work
   - Frontend work
   - Authentication & security
   - Database setup
   - Integration & testing
3. Respect spec-driven development:
   - Each step must reference relevant specs using @specs/... paths.
   - No implementation before specs are complete.
4. Ensure correct dependency order:
   - Database schema before API routes
   - Auth before securing endpoints
   - Backend APIs before frontend integration
5. Align with monorepo structure:
   - /backend
   - /frontend
   - Shared environment variables

Milestones to Plan:
Milestone 1: Repository & Environment Setup
- Verify monorepo structure
- Backend and frontend project initialization
- Environment variables and secrets setup

Milestone 2: Database & Models
- PostgreSQL connection via Neon
- SQLModel task schema
- User-to-task relationship

Milestone 3: Backend Core APIs
- CRUD endpoints for tasks
- Request/response models
- Error handling

Milestone 4: Authentication & Authorization
- Better Auth JWT configuration (frontend)
- JWT verification middleware (FastAPI)
- User scoping and ownership enforcement

Milestone 5: Frontend Core Features
- Authentication UI (signup/signin)
- Task list, create, update, delete UI
- API client with JWT injection

Milestone 6: Integration & Validation
- End-to-end user flow testing
- Auth failure cases (401 handling)
- Data isolation between users

Output Expectations:
- A numbered, sequential plan
- Each step references the relevant spec(s)
- Clear indication of inputs/outputs for each step
- No code, only an execution plan
- Ready to be followed by Claude Code for implementation

Do NOT write implementation code.
Only produce a clean, detailed Phase II execution plan aligned with the specs.

## Response snapshot

Created comprehensive development tasks for the Todo Full-Stack Web Application (Phase II), organized into 6 phases following the user story priorities:

- Phase 1: Setup (T001-T006) - Repository & Environment Setup
- Phase 2: Foundational Components (T007-T012) - Database & Models
- Phase 3: [US1] User Authentication (T013-T022) - Authentication & Authorization
- Phase 4: [US2] Personal Task Management (T023-T038) - Backend Core APIs & Frontend Features
- Phase 5: [US3] Task Status Management (T039-T045) - Additional Frontend Features
- Phase 6: Polish & Cross-Cutting Concerns (T046-T060) - Integration & Validation

All tasks follow the required checklist format with proper IDs, story labels, and file paths. Tasks are organized by user story to enable independent implementation and testing.

## Outcome

- ✅ Impact: Complete task breakdown created for full-stack todo application implementation
- 🧪 Tests: Tasks validated against plan and specification requirements
- 📁 Files: 1 tasks document with 60+ specific, executable tasks
- 🔁 Next prompts: Ready for implementation following the task list
- 🧠 Reflection: Tasks organized by user stories with proper dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Tasks meet all requirements
- Prompt variant (if applicable): Standard tasks generation prompt
- Next experiment (smallest change to try): Begin implementation with Phase 1 tasks
