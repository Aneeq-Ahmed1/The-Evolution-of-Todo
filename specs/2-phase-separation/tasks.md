# Implementation Tasks: Phase 1 and Phase 2 Separation

**Feature**: Phase 1 and Phase 2 Separation
**Branch**: `2-phase-separation`
**Created**: 2026-01-08

## Overview
This document outlines the tasks required to separate Phase 1 (console app) and Phase 2 (web app) into isolated directory structures while maintaining all existing functionality.

## Implementation Strategy
- **MVP First**: Complete User Story 1 (Organized Project Structure) first to establish the foundation
- **Incremental Delivery**: Each user story builds upon the previous ones
- **Independent Testing**: Each user story can be tested independently
- **Zero Downtime**: Maintain existing functionality throughout the refactoring

## Dependencies
- User Story 1 (P1) must be completed before User Story 2 (P1)
- User Story 2 (P1) must be completed before User Story 3 (P2)
- User Story 3 (P2) must be completed before User Story 4 (P2)

## Parallel Execution Examples
- [P] tasks within each user story can be executed in parallel if they modify different files/components
- Backend import updates can be done in parallel with frontend path updates

## Phase 1: Setup Tasks
Goal: Establish the foundational directory structure

- [X] T001 Create phase-1-console/ directory at repository root
- [X] T002 Create phase-2-web/ directory at repository root (will be accessed as phase_2_web in Python)
- [X] T003 Create phase-2-web/frontend/ directory
- [X] T004 Create phase-2-web/backend/ directory

## Phase 2: Foundational Tasks
Goal: Set up the core structure needed for both phases

- [X] T005 [P] Move src/ directory to phase-1-console/src/ (Phase 1 console app)
- [X] T006 [P] Move backend/ directory to phase-2-web/backend/ (Phase 2 backend) - note: will be accessed as phase_2_web.backend in Python
- [X] T007 [P] Move frontend/ directory to phase-2-web/frontend/ (Phase 2 frontend)
- [X] T008 Update run_backend.py to import from new backend location (phase_2_web.backend.main)

## Phase 3: User Story 1 - Organized Project Structure (Priority: P1)
Goal: Ensure Phase 1 and Phase 2 files are properly isolated in their respective directories

**Independent Test**: Verify that Phase 1 files are in phase-1-console/ and Phase 2 files are in phase-2-web/ with proper frontend/backend separation.

- [X] T009 [US1] Verify all Phase 1 console-related files are in phase-1-console/src/todo/
- [X] T010 [US1] Verify all Phase 2 backend files are in phase-2-web/backend/
- [X] T011 [US1] Verify all Phase 2 frontend files are in phase-2-web/frontend/
- [X] T012 [US1] Confirm pyproject.toml remains at repository root (no duplication)
- [X] T013 [US1] Update README.md to document the new directory structure

## Phase 4: User Story 2 - Backend Continues to Function (Priority: P1)
Goal: Ensure the backend continues to run after structural changes with no breaking functionality

**Independent Test**: The backend can be started with the command `uv run uvicorn phase_2_web.backend.main:app --reload --port 8000` and serves requests as expected.

- [X] T014 [US2] Update backend import paths from `backend.*` to `phase_2_web.backend.*` in main.py (adjust for new directory structure)
- [X] T015 [US2] Update backend import paths in routes/auth.py (adjust for new directory structure)
- [X] T016 [US2] Update backend import paths in routes/tasks.py (adjust for new directory structure)
- [X] T017 [US2] Update backend import paths in services/ (if any exist) (adjust for new directory structure)
- [X] T018 [US2] Update backend import paths in db.py (adjust for new directory structure)
- [X] T019 [US2] Update backend import paths in models.py (adjust for new directory structure)
- [X] T020 [US2] Update backend import paths in schemas.py (adjust for new directory structure)
- [X] T021 [US2] Update backend import paths in settings.py (adjust for new directory structure)
- [X] T022 [US2] Update uvicorn command to work with new structure: `uv run uvicorn phase_2_web.backend.main:app --reload --port 8000`
- [X] T023 [US2] Verify Neon database connectivity works after refactoring
- [X] T024 [US2] Test API endpoints to ensure responses are returned without errors

## Phase 5: User Story 3 - Import Paths Updated (Priority: P2)
Goal: Update all import paths to reflect new file locations so the code continues to function correctly

**Independent Test**: The application can be run without import errors after the refactoring.

- [X] T025 [US3] Update import paths in run_backend.py to reference new backend location
- [X] T026 [US3] Update any test files that reference old import paths
- [X] T027 [US3] Update import paths in any configuration files
- [X] T028 [US3] Verify all Python files import successfully without errors
- [X] T029 [US3] Run existing tests to ensure no import-related failures

## Phase 6: User Story 4 - Deployment Compatibility Maintained (Priority: P2)
Goal: Maintain Hugging Face deployment compatibility so the deployment process continues to work without changes

**Independent Test**: The application can be deployed to Hugging Face as before the refactoring.

- [X] T030 [US4] Verify pyproject.toml at root contains correct backend path for deployment
- [X] T031 [US4] Update any deployment configuration files to reference new structure
- [X] T032 [US4] Test deployment command: `uv run uvicorn phase_2_web.backend.main:app --host 0.0.0.0 --port 7860`
- [X] T033 [US4] Verify all necessary files are accessible for deployment
- [X] T034 [US4] Update Dockerfile if needed to accommodate new structure

## Phase 7: Polish & Cross-Cutting Concerns
Goal: Final verification and cleanup to ensure everything works as expected

- [X] T035 Verify all existing tests pass with new structure
- [X] T036 Clean up any temporary files created during migration
- [X] T037 Update any documentation to reflect new structure
- [X] T038 Run full integration test suite
- [X] T039 Verify Phase 1 console app still functions correctly
- [X] T040 Perform final verification of all acceptance criteria
- [X] T041 Update gitignore if needed for new structure
- [X] T042 Document any breaking changes for developers (if any)