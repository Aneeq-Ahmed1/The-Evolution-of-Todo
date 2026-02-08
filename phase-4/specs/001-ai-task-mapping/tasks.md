# Tasks: AI Task Display Mapping

**Input**: Design documents from `/specs/001-ai-task-mapping/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `agents/backend/src/`
- Paths shown below match the monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for display mapping functionality

- [x] T001 Review existing task management architecture in backend/src/api/tasks.py to understand current implementation
- [x] T002 [P] Document current task display mechanism in frontend/src/components/TaskList.tsx
- [x] T003 [P] Analyze AI agent intent parsing logic in agents/backend/src/services/intent_parser.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create display mapping TypeScript types in frontend/src/types/mapping.ts
- [x] T005 [P] Create display mapping Pydantic schemas in backend/src/schemas/mapping.py
- [x] T006 [P] Implement ordinal resolver utility module in agents/backend/src/services/ordinal_resolver.py
- [x] T007 Create display mapping service in frontend/src/services/displayMappingService.ts
- [x] T008 [P] Create task resolver service in agents/backend/src/services/task_resolver.py
- [x] T009 Add mapping refresh endpoint POST /mapping/refresh in backend/src/api/mapping.py
- [x] T010 [P] Add resolve display index endpoint POST /mapping/resolve in backend/src/api/mapping.py
- [x] T011 Register mapping router in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Recognize Task Numbers in AI Commands (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with specific tasks using display numbers (e.g., "task 1 is complete", "edit task 2") and have the AI agent correctly identify and act on the intended task.

**Independent Test**: User can say "task 1 is complete" after viewing tasks displayed as "1. Buy groceries", "2. Pay bills" and the system correctly marks the grocery task (first displayed) as completed regardless of internal task_id.

### Implementation for User Story 1

- [x] T012 [P] [US1] Modify GET /tasks endpoint to include display_index in response in backend/src/api/tasks.py
- [x] T013 [P] [US1] Update TaskService.get_user_tasks() to assign sequential display_index (1-based) in backend/src/services/task_service.py
- [x] T014 [US1] Update TaskList component to maintain display_index → task_id mapping state in frontend/src/components/TaskList.tsx
- [x] T015 [US1] Implement generateDisplayMapping() function in frontend/src/services/displayMappingService.ts
- [x] T016 [US1] Update AI agent intent parser to recognize numeric task references ("task 1", "task 2") in agents/backend/src/services/intent_parser.py
- [x] T017 [US1] Implement parseNumericTaskReference() in agents/backend/src/services/ordinal_resolver.py
- [x] T018 [US1] Update todo_agent to use display_index for task resolution in agents/backend/src/agents/todo_agent.py
- [x] T019 [US1] Implement resolveDisplayIndex() in agents/backend/src/services/task_resolver.py
- [x] T020 [US1] Add GET /tasks/display/{display_index} endpoint in backend/src/api/tasks.py
- [x] T021 [US1] Update complete task action to support display_index parameter in backend/src/api/tasks.py
- [x] T022 [US1] Add PATCH /tasks/display/{display_index}/completion endpoint in backend/src/api/tasks.py
- [x] T023 [US1] Implement validateDisplayIndex() in backend/src/services/task_service.py
- [x] T024 [US1] Update frontend to refresh display mapping after task list changes in frontend/src/services/displayMappingService.ts
- [x] T025 [US1] Add error handling for invalid display_index in backend/src/api/tasks.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can say "task 1 is complete" or "edit task 2" and the system correctly identifies and acts on the intended task.

---

## Phase 4: User Story 2 - Handle Ordinal References (Priority: P2)

**Goal**: Enable users to use various ordinal expressions (e.g., "first task", "second task", "task one") and have the AI correctly identify the intended task based on display order.

**Independent Test**: User can say "first task is complete" after viewing tasks and the system correctly identifies and marks the first displayed task as completed.

### Implementation for User Story 2

- [x] T026 [P] [US2] Implement parseOrdinalWordReference() to handle "first", "second", "third" in agents/backend/src/services/ordinal_resolver.py
- [x] T027 [P] [US2] Implement parseNumberWordReference() to handle "one", "two", "three" in agents/backend/src/services/ordinal_resolver.py
- [x] T028 [US2] Update intent parser to recognize ordinal word patterns in agents/backend/src/services/intent_parser.py
- [x] T029 [US2] Add support for ordinal suffixes ("1st task", "2nd task", "3rd task") in agents/backend/src/services/ordinal_resolver.py
- [x] T030 [US2] Create normalizeOrdinalToNumber() to convert all ordinal formats to integers in agents/backend/src/services/ordinal_resolver.py
- [x] T031 [US2] Update todo_agent to use normalizeOrdinalToNumber() before display_index resolution in agents/backend/src/agents/todo_agent.py
- [x] T032 [US2] Add validation for ordinal format variations in agents/backend/src/services/ordinal_resolver.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can use "task 1", "first task", or "task one" interchangeably.

---

## Phase 5: User Story 3 - Error Handling for Invalid Task Numbers (Priority: P3)

**Goal**: Provide helpful feedback when users reference task numbers that don't exist or are out of range, avoiding generic "I'm not sure what you mean" responses.

**Independent Test**: User says "task 100 is complete" when only 3 tasks are displayed, and the system provides helpful error feedback like "You only have 3 tasks. Did you mean task 1, 2, or 3?"

### Implementation for User Story 3

- [x] T033 [P] [US3] Implement validateIndexRange() to check if display_index exists in current mapping in backend/src/services/task_service.py
- [x] T034 [P] [US3] Create helpful error message generator for out-of-range indices in agents/backend/src/services/task_resolver.py
- [x] T035 [US3] Update todo_agent to provide confident error responses when intent is clear in agents/backend/src/agents/todo_agent.py
- [x] T036 [US3] Add error handling for empty task list scenario in agents/backend/src/services/task_resolver.py
- [x] T037 [US3] Implement getTaskCountMessage() to include current task count in error responses in agents/backend/src/services/task_resolver.py
- [x] T038 [US3] Update frontend to display inline validation feedback for invalid references in frontend/src/components/TaskList.tsx
- [x] T039 [US3] Add fallback error handling for ambiguous task references in agents/backend/src/agents/todo_agent.py

**Checkpoint**: All user stories should now be independently functional with robust error handling.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T040 [P] Update API documentation with display mapping endpoints in backend/src/main.py
- [x] T041 [P] Add logging for display_index resolution operations in agents/backend/src/services/task_resolver.py
- [x] T042 Add documentation comments to ordinal resolver functions in agents/backend/src/services/ordinal_resolver.py
- [x] T043 [P] Update CLAUDE.md with display mapping usage patterns in CLAUDE.md
- [x] T044 Update TaskList component with accessibility labels for screen readers in frontend/src/components/TaskList.tsx
- [x] T045 [P] Add performance monitoring for mapping refresh operations in frontend/src/services/displayMappingService.ts
- [x] T046 Verify quickstart.md instructions work with display mapping feature in specs/001-ai-task-mapping/quickstart.md
- [x] T047 Code cleanup and refactoring for ordinal resolution logic in agents/backend/src/services/ordinal_resolver.py
- [x] T048 [P] Ensure display mapping persists correctly during user session in frontend/src/services/displayMappingService.ts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 & US2 but independently testable

### Within Each User Story

- Models/Types before services
- Services before API endpoints
- Backend endpoints before frontend integration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tasks marked [P] within each user story can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch foundational parallel tasks together:
Task: "Create display mapping Pydantic schemas in backend/src/schemas/mapping.py"
Task: "Implement ordinal resolver utility module in agents/backend/src/services/ordinal_resolver.py"
Task: "Create task resolver service in agents/backend/src/services/task_resolver.py"
Task: "Add resolve display index endpoint POST /mapping/resolve in backend/src/api/mapping.py"

# Launch US1 parallel tasks together:
Task: "Modify GET /tasks endpoint to include display_index in response in backend/src/api/tasks.py"
Task: "Update TaskService.get_user_tasks() to assign sequential display_index in backend/src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T012-T025)
4. **STOP and VALIDATE**: Test that "task 1 is complete" and "edit task 2" work correctly
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! Users can use "task 1", "task 2")
3. Add User Story 2 → Test independently → Deploy/Demo (Now "first task", "second task" also work)
4. Add User Story 3 → Test independently → Deploy/Demo (Now helpful error messages for invalid references)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (numeric references)
   - Developer B: User Story 2 (ordinal words)
   - Developer C: User Story 3 (error handling)
3. Stories complete and integrate independently

---

## Success Metrics

After implementation, verify these metrics from spec.md:

- **SC-001**: 95% of ordinal task references (e.g., "task 1 is complete") correctly resolve to the intended task
- **SC-002**: 95% of edit commands using ordinal references (e.g., "edit task 2") successfully update the correct task
- **SC-003**: 95% of completion toggle commands using ordinal references work correctly
- **SC-004**: Error response time for invalid task references is under 1 second
- **SC-005**: AI agent provides helpful error messages instead of "I'm not sure" responses with 90% confidence
- **SC-006**: System handles duplicate task titles correctly when using ordinal references with 95% accuracy
- **SC-007**: Display-index to task_id mapping updates correctly after task list modifications
- **SC-008**: User satisfaction rating for task reference commands is 4.0/5.0 or higher
- **SC-009**: Task reference commands work consistently across different ordinal formats

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Display mapping must stay synchronized between UI and AI agent contexts
- Runtime mapping should be lightweight and performant (no database storage needed)
