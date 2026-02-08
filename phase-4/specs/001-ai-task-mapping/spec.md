# Feature Specification: AI Task Display Mapping

**Feature Branch**: `001-ai-task-mapping`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "/sp.specify

Issue Diagnosis Update:

The AI agent fails to recognize commands like:
- "task 1 is complete"
- "edit task 2"

Root Cause:
- The AI does not understand task numbers shown to the user
- Displayed task numbers (1,2,3) are not mapped to internal task_id
- Intent parser does not handle ordinal references (task 1, second task)

Required Fix:

1. Task Display Mapping
- When listing tasks, assign a display_index (1-based)
- Maintain a runtime mapping:
  display_index → task_id

2. Intent Understanding Enhancement
- AI must recognize ordinal references:
  "task 1", "task one", "first task", "second task"
- Extract intent + display_index from user message

3. Resolution Logic
- Convert display_index to task_id using mapping
- Execute action strictly using task_id

4. Action Support
- COMPLETE: mark completed = true
- UNCOMPLETE: mark completed = false
- EDIT: ask for new content if missing
- DELETE: remove task by task_id

5. Validation
- If index is invalid, respond with helpful error
- Never say "I'm not sure what you mean" if intent is clear

Acceptance Criteria:
- "task 1 is complete" works
- "edit task 2" triggers edit flow
- Duplicate task titles do not cause failure
- AI responds confidently and correctly

Constraint:
- Do not change task creation logic
- Fix intent parsing and index-to-id resolution only"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recognize Task Numbers in AI Commands (Priority: P1)

User wants to interact with specific tasks using the numbers they see on screen (e.g., "task 1 is complete", "edit task 2") and expects the AI agent to understand these ordinal references and perform the correct action on the intended task.

**Why this priority**: This is the core functionality that enables users to efficiently interact with tasks using natural language commands that reference visible task numbers.

**Independent Test**: User can say "task 1 is complete" and the system correctly marks the first displayed task as completed, regardless of its internal task_id.

**Acceptance Scenarios**:

1. **Given** user has tasks displayed as "1. Buy groceries", "2. Pay bills", "3. Schedule meeting", **When** user says "task 1 is complete", **Then** the grocery task is marked as completed.

2. **Given** user has tasks displayed with numbers, **When** user says "edit task 2" followed by new content, **Then** the second displayed task is updated with the new content.

---

### User Story 2 - Handle Ordinal References (Priority: P2)

User wants to use various ordinal expressions (e.g., "first task", "second task", "task one") and expects the AI to correctly identify the intended task based on the display order.

**Why this priority**: Expands the natural language capabilities to match how users naturally speak about tasks.

**Independent Test**: User can say "first task is complete" and the system correctly identifies and marks the first displayed task as completed.

**Acceptance Scenarios**:

1. **Given** user has tasks displayed in order, **When** user says "first task is complete", **Then** the first displayed task is marked as completed.

2. **Given** user has tasks displayed in order, **When** user says "third task" with an action, **Then** the third displayed task receives the action.

---

### User Story 3 - Error Handling for Invalid Task Numbers (Priority: P3)

User might reference a task number that doesn't exist or is out of range, and expects the AI to provide helpful feedback rather than saying "I'm not sure what you mean".

**Why this priority**: Ensures robust error handling and provides good user experience when invalid references are made.

**Independent Test**: User says "task 100 is complete" when only 3 tasks are displayed, and the system provides helpful error feedback.

**Acceptance Scenarios**:

1. **Given** user has 3 tasks displayed, **When** user says "task 5 is complete", **Then** the system responds with a helpful error message about the invalid task number.

2. **Given** user makes an ambiguous reference, **When** intent is clear from context, **Then** the system acts confidently rather than asking for clarification unnecessarily.

---

### Edge Cases

- What happens when user references a task number that is out of range (e.g., "task 10" when only 3 tasks exist)?
- How does system handle duplicate task titles when user says "edit the grocery task"?
- What occurs when user says "first task" but there are no tasks displayed?
- How does the system handle ordinal references in different languages or formats (e.g., "1st task", "one", "uno")?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST assign display_index to each task when listing (1-based sequential numbering)
- **FR-002**: System MUST maintain runtime mapping between display_index and internal task_id
- **FR-003**: AI agent MUST recognize ordinal task references ("task 1", "first task", "second task", "task one")
- **FR-004**: System MUST extract intent and display_index from user commands containing ordinal references
- **FR-005**: System MUST convert display_index to task_id using the runtime mapping before executing actions
- **FR-006**: System MUST support COMPLETE action (set completed = true) using display_index mapping
- **FR-007**: System MUST support UNCOMPLETE action (set completed = false) using display_index mapping
- **FR-008**: System MUST support EDIT action using display_index mapping
- **FR-009**: System MUST support DELETE action using display_index mapping
- **FR-010**: System MUST provide helpful error messages when display_index is invalid or out of range
- **FR-011**: AI agent MUST respond confidently when intent is clear, avoiding generic "I'm not sure" responses
- **FR-012**: System MUST handle duplicate task titles without confusion when using display_index references
- **FR-013**: Runtime mapping MUST be refreshed when task list changes (add/delete/reorder operations)

### Key Entities

- **Display Mapping**: Runtime association between display_index (1-based) and internal task_id, maintained per user session
- **Ordinal Reference**: Natural language patterns that refer to tasks by position ("task 1", "first task", "second task", etc.)
- **Task Resolution**: Process of converting a display_index from user input to internal task_id for backend operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of ordinal task references (e.g., "task 1 is complete") correctly resolve to the intended task
- **SC-002**: 95% of edit commands using ordinal references (e.g., "edit task 2") successfully update the correct task
- **SC-003**: 95% of completion toggle commands using ordinal references work correctly
- **SC-004**: Error response time for invalid task references is under 1 second
- **SC-005**: AI agent provides helpful error messages instead of "I'm not sure" responses with 90% confidence
- **SC-006**: System handles duplicate task titles correctly when using ordinal references with 95% accuracy
- **SC-007**: Display-index to task_id mapping updates correctly after task list modifications
- **SC-008**: User satisfaction rating for task reference commands is 4.0/5.0 or higher
- **SC-009**: Task reference commands work consistently across different ordinal formats ("task 1", "first task", "task one")