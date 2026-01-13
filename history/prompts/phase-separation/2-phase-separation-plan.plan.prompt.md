---
id: 2
title: phase-separation-plan
stage: plan
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase-separation
branch: 2-phase-separation
user: Da-Bros
command: /sp.plan
labels: [planning,refactor,structure]
links:
  spec: specs/2-phase-separation/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/2-phase-separation/plan.md
 - specs/2-phase-separation/research.md
 - specs/2-phase-separation/data-model.md
 - specs/2-phase-separation/quickstart.md
 - specs/2-phase-separation/contracts/api-contract.md
tests:
 - research.md validates current structure
 - data-model.md documents entities
 - quickstart.md guides usage
---

## Prompt

Goal:
Refactor repository to separate Phase 1 and Phase 2, keeping Phase 2 backend fully working.

Step-by-step plan:

1. Create two top-level folders:
   - phase-1-console/
   - phase-2-web/

2. Move all Phase 1 console-related files to phase-1-console/

3. Move current frontend and backend files to phase-2-web/frontend and phase-2-web/backend

4. Ensure pyproject.toml remains at root

5. Update backend import paths:
   - All `from src.` → `from backend.` if necessary

6. Verify backend runs locally:
   - uv run uvicorn phase-2-web.backend.main:app --reload --port 8000

7. Verify frontend runs locally:
   - cd phase-2-web/frontend && npm run dev

8. Test database connection to Neon:
   - Ensure JWT auth still works
   - Ensure tasks and users are accessible

9. Document folder structure in README

10. Prepare for Hugging Face deployment:
    - Ensure `pyproject.toml` at root
    - backend folder ready to run independently

Acceptance Criteria:
- Phase 1 & Phase 2 isolated
- Backend and frontend fully functional
- Neon DB and JWT auth work
- HF deployment ready

## Response snapshot

Completed comprehensive planning for the phase separation feature. Created multiple artifacts:

1. **Implementation Plan** (plan.md): Detailed technical context and project structure
2. **Research Document** (research.md): Analysis of current codebase structure and migration requirements
3. **Data Model** (data-model.md): Documentation of both Phase 1 and Phase 2 data models
4. **Quickstart Guide** (quickstart.md): Instructions for running both applications after separation
5. **API Contracts** (contracts/api-contract.md): Detailed API specification for Phase 2 backend

Key decisions made:
- Phase 1 console app will be moved to phase-1-console/src/todo/
- Phase 2 will be organized as phase-2-web/{frontend,backend}/
- pyproject.toml remains at repository root for deployment compatibility
- Backend import paths will be updated to reflect new structure
- All existing functionality must remain intact

The plan ensures that:
- Minimal change principle is followed (structural refactor only)
- Backward compatibility is maintained
- Security patterns (JWT auth) remain unchanged
- Hugging Face deployment compatibility is preserved
- All existing tests continue to pass

## Outcome

- ✅ Impact: Comprehensive plan created for phase separation refactor
- 🧪 Tests: All planning artifacts validated and documented
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/api-contract.md
- 🔁 Next prompts: Ready for /sp.tasks to create implementation tasks
- 🧠 Reflection: Plan addresses all requirements while maintaining existing functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All planning artifacts complete
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation phase