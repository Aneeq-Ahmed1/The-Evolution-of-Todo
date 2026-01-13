# Implementation Plan: Phase 1 and Phase 2 Separation

**Branch**: `2-phase-separation` | **Date**: 2026-01-08 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/2-phase-separation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Structural refactoring to separate Phase 1 console application and Phase 2 web application into isolated directory structures. This involves moving files to new locations (phase-1-console/ and phase-2-web/) while maintaining all existing functionality, particularly ensuring the Phase 2 backend continues to work with the Neon database and JWT authentication.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for frontend
**Primary Dependencies**: FastAPI, uv, Neon database, JWT authentication
**Storage**: Neon PostgreSQL database
**Testing**: pytest for backend, Jest for frontend (if applicable)
**Target Platform**: Web application with console app separation
**Project Type**: Full-stack web application with console components
**Performance Goals**: Maintain current performance levels with no degradation
**Constraints**: Must preserve all existing functionality, maintain deployment compatibility
**Scale/Scope**: Same as current application (single user/todo app with JWT auth)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Minimal Change Principle: This is a structural refactor without changing logic
- [x] Backward Compatibility: All existing functionality must remain intact
- [x] Dependency Management: pyproject.toml stays at root, no new dependencies
- [x] Security: No changes to JWT authentication or database access patterns
- [x] Testing: All existing tests should continue to pass

### Post-Design Constitution Check

- [x] API Contract Consistency: API endpoints remain unchanged functionally
- [x] Data Model Integrity: Both Phase 1 and Phase 2 data models preserved
- [x] Deployment Compatibility: Hugging Face deployment remains functional
- [x] Import Path Resolution: Backend import paths will be updated appropriately

## Project Structure

### Documentation (this feature)

```text
specs/2-phase-separation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-1-console/
├── [existing console app files moved here]

phase-2-web/
├── frontend/
│   ├── [existing frontend files moved here]
│   ├── package.json
│   └── src/
└── backend/
    ├── main.py
    ├── src/
    │   ├── models/
    │   ├── services/
    │   └── routes/
    ├── requirements.txt
    └── tests/

pyproject.toml              # Remains at root
README.md                   # Updated to reflect new structure
uv.lock                     # Remains at root
```

**Structure Decision**: Selected Option 2: Web application structure with separated console app. The phase-1-console/ directory contains all console-related files, while phase-2-web/ contains both frontend/ and backend/ directories for the web application. The pyproject.toml remains at the repository root to maintain compatibility with uv and Hugging Face deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| File movement | Structural organization | Keeping mixed files would make maintenance harder |
| Import path updates | Required for new structure | No alternative to updating imports after file moves |