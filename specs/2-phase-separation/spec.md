# Feature Specification: Phase 1 and Phase 2 Separation

**Feature Branch**: `2-phase-separation`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Goal:
Separate Phase 1 (console app) and Phase 2 (full-stack web app)
into clean, isolated folders without breaking the working Phase 2 backend.

Requirements:
1. Create two top-level folders:
   - phase-1-console/
   - phase-2-web/

2. Move all Phase 1 console-related files into:
   phase-1-console/

3. Move all current frontend and backend code into:
   phase-2-web/
   ├── frontend/
   └── backend/

4. Keep pyproject.toml at repository ROOT
   - Do NOT duplicate it inside backend
   - Backend must continue to run with:
     uv run uvicorn phase-2-web.backend.main:app --reload --port 8000

5. Update all import paths to remain valid
6. Do NOT change any working logic
7. Ensure Hugging Face deployment remains compatible

Acceptance Criteria:
- Phase 1 and Phase 2 are fully isolated
- Backend runs successfully from repo root
- Neon database still works
- No breaking changes

Notes:
This is a structural refactor only.
No new features. No deletions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organized Project Structure (Priority: P1)

As a developer, I want to have Phase 1 console app and Phase 2 web app separated into distinct folders so that I can easily navigate and maintain each phase independently.

**Why this priority**: This is the core requirement of the feature and enables proper isolation between the two phases of the project.

**Independent Test**: The project structure can be verified by checking that Phase 1 files are in phase-1-console/ and Phase 2 files are in phase-2-web/ with proper frontend/backend separation.

**Acceptance Scenarios**:

1. **Given** a repository with mixed Phase 1 and Phase 2 files, **When** the refactoring is complete, **Then** Phase 1 files are located in phase-1-console/ directory
2. **Given** a repository with mixed Phase 1 and Phase 2 files, **When** the refactoring is complete, **Then** Phase 2 frontend files are located in phase-2-web/frontend/ directory
3. **Given** a repository with mixed Phase 1 and Phase 2 files, **When** the refactoring is complete, **Then** Phase 2 backend files are located in phase-2-web/backend/ directory

---

### User Story 2 - Backend Continues to Function (Priority: P1)

As a developer, I want the backend to continue running after the structural changes so that there are no breaking changes to the existing functionality.

**Why this priority**: Maintaining existing functionality is critical to ensure no disruption to current users.

**Independent Test**: The backend can be started with the command `uv run uvicorn phase-2-web.backend.main:app --reload --port 8000` and serves requests as expected.

**Acceptance Scenarios**:

1. **Given** the refactored project structure, **When** running `uv run uvicorn phase-2-web.backend.main:app --reload --port 8000`, **Then** the backend server starts successfully
2. **Given** the running backend server, **When** making API requests, **Then** responses are returned as expected without errors

---

### User Story 3 - Import Paths Updated (Priority: P2)

As a developer, I want all import paths to be updated after the structural changes so that the code continues to function correctly.

**Why this priority**: Without proper import path updates, the application would fail with import errors.

**Independent Test**: The application can be run without import errors after the refactoring.

**Acceptance Scenarios**:

1. **Given** the refactored project structure, **When** importing modules, **Then** all imports resolve correctly without errors

---

### User Story 4 - Deployment Compatibility Maintained (Priority: P2)

As a developer, I want to maintain Hugging Face deployment compatibility so that the deployment process continues to work without changes.

**Why this priority**: Maintaining deployment compatibility ensures no disruption to the release process.

**Independent Test**: The application can be deployed to Hugging Face as before the refactoring.

**Acceptance Scenarios**:

1. **Given** the refactored project structure, **When** deploying to Hugging Face, **Then** the deployment succeeds without configuration changes

---

### Edge Cases

- What happens when external tools or scripts reference the old file paths?
- How does the system handle relative path references in configuration files?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create a phase-1-console/ directory at the repository root
- **FR-002**: System MUST create a phase-2-web/ directory at the repository root
- **FR-003**: System MUST move all Phase 1 console-related files into phase-1-console/ directory
- **FR-004**: System MUST create phase-2-web/frontend/ directory for frontend code
- **FR-005**: System MUST create phase-2-web/backend/ directory for backend code
- **FR-006**: System MUST move all current frontend code into phase-2-web/frontend/
- **FR-007**: System MUST move all current backend code into phase-2-web/backend/
- **FR-008**: System MUST keep pyproject.toml at repository root (not duplicate in backend)
- **FR-009**: System MUST update all import paths to reflect new file locations
- **FR-010**: System MUST maintain all existing functionality without changes
- **FR-011**: System MUST ensure backend runs with command: uv run uvicorn phase-2-web.backend.main:app --reload --port 8000
- **FR-012**: System MUST preserve Neon database connectivity and functionality
- **FR-013**: System MUST maintain Hugging Face deployment compatibility

### Key Entities *(include if feature involves data)*

- **Phase 1 Console App**: Collection of files related to the console application functionality
- **Phase 2 Web App**: Collection of frontend and backend files related to the full-stack web application
- **Backend Configuration**: Project configuration files and dependencies that must remain at root level

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Phase 1 and Phase 2 code are fully isolated in separate directories with no cross-contamination
- **SC-002**: Backend runs successfully from repository root with the specified command: uv run uvicorn phase-2-web.backend.main:app --reload --port 8000
- **SC-003**: All existing functionality continues to work without any breaking changes
- **SC-004**: Neon database connectivity remains functional after the structural changes
- **SC-005**: Deployment to Hugging Face continues to work without configuration changes
- **SC-006**: Import paths are correctly updated and all modules can be imported without errors