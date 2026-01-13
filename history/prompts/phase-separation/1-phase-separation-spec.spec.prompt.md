---
id: 1
title: phase-separation-spec
stage: spec
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase-separation
branch: 2-phase-separation
user: Da-Bros
command: /sp.specify
labels: [specification,refactor,structure]
links:
  spec: specs/2-phase-separation/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/2-phase-separation/spec.md
 - specs/2-phase-separation/checklists/requirements.md
tests:
 - specs/2-phase-separation/spec.md validated
 - checklists/requirements.md created
---

## Prompt

Goal:
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
No new features. No deletions.

## Response snapshot

Created a comprehensive specification for separating Phase 1 (console app) and Phase 2 (full-stack web app) into clean, isolated folders. The specification includes:

- User scenarios and testing requirements with priorities
- Functional requirements (FR-001 through FR-013) covering all structural changes needed
- Success criteria (SC-001 through SC-006) that are measurable and technology-agnostic
- Key entities and edge cases
- A quality checklist to validate the specification

The spec ensures that:
- Phase 1 files go to phase-1-console/ directory
- Phase 2 files go to phase-2-web/ with frontend/backend separation
- Backend continues to run with the specified command
- Import paths are updated correctly
- No breaking changes are introduced
- Deployment compatibility is maintained

## Outcome

- ✅ Impact: Created complete specification for phase separation refactor
- 🧪 Tests: Spec validated against quality criteria checklist
- 📁 Files: Created spec.md and requirements.md checklist
- 🔁 Next prompts: Ready for /sp.plan to implement the structural changes
- 🧠 Reflection: Specification is comprehensive and addresses all requirements without implementation details

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All quality criteria met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase