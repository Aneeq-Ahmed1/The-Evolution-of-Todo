# Implementation Plan: AI Task Display Mapping

**Branch**: `001-ai-task-mapping` | **Date**: 2026-01-04 | **Spec**: [specs/001-ai-task-mapping/spec.md](specs/001-ai-task-mapping/spec.md)
**Input**: Feature specification from `/specs/001-ai-task-mapping/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of task display mapping functionality to enable AI agent to recognize and respond to ordinal task references (e.g., "task 1 is complete", "edit task 2"). The solution will establish a runtime mapping between display indices and internal task IDs, enhance intent parsing for ordinal references, and ensure deterministic AI behavior with confident responses.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend, Next.js 15+
**Primary Dependencies**: FastAPI backend, Next.js frontend, SQLModel ORM, Neon PostgreSQL, React
**Storage**: Neon PostgreSQL cloud database with existing task schema
**Testing**: Jest for frontend, pytest for backend, manual integration testing
**Target Platform**: Web application (Next.js + FastAPI) with responsive UI
**Project Type**: Full-stack web application (existing architecture)
**Performance Goals**: <500ms API response time, <2s page load, 95% task operation success rate
**Constraints**: Must maintain existing task creation flow, preserve UI consistency, ensure data integrity
**Scale/Scope**: Multi-user support with individual task isolation, up to 1000 tasks per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All constitution requirements pass:
- ✅ No new repositories needed (using existing monorepo structure)
- ✅ No new languages introduced (using existing Python/TypeScript stack)
- ✅ No architectural changes required (extending existing patterns)
- ✅ No security violations (following existing auth patterns)
- ✅ No dependency conflicts (using existing tech stack)

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-task-mapping/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── mapping.py  # NEW: Display mapping endpoints
│   └── schemas/
│       ├── auth.py
│       └── task.py

frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   └── tasks/
│   │   │       └── page.tsx
│   │   ├── auth/
│   │   └── admin/
│   ├── components/
│   │   ├── TaskList.tsx
│   │   └── TaskForm.tsx
│   ├── services/
│   │   ├── taskService.ts
│   │   └── displayMappingService.ts  # NEW: Display mapping service
│   ├── lib/
│   │   ├── auth.ts
│   │   └── api.ts
│   └── types/
│       ├── task.ts
│       └── mapping.ts  # NEW: Display mapping types

agents/
├── backend/
│   └── src/
│       ├── agents/
│       │   ├── todo_agent.py
│       │   └── ordinal_resolver.py  # NEW: Ordinal resolution service
│       └── services/
│           ├── intent_parser.py
│           └── task_resolver.py     # NEW: Task resolution service
```

**Structure Decision**: Using existing full-stack web application structure with Next.js frontend and FastAPI backend. Adding new modules for display mapping functionality without architectural changes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Architecture Analysis & Research

### 0.1 Current State Analysis
- **Research Task**: Analyze current AI agent task reference implementation
- **Research Task**: Identify root cause of ordinal reference misrecognition
- **Research Task**: Document current task display and indexing mechanism

### 0.2 Technology Investigation
- **Research Task**: Review ordinal number parsing libraries and patterns
- **Research Task**: Investigate runtime mapping data structures for display_index → task_id
- **Research Task**: Research natural language processing for ordinal references

### 0.3 Research Output
- **Deliverable**: research.md with findings on current implementation gaps
- **Deliverable**: Root cause analysis of why ordinal references fail
- **Deliverable**: Recommended approach for display mapping implementation

## Phase 1: Design & Contracts

### 1.1 Data Model Design
- **Task**: Define display mapping entity with display_index and task_id relationship
- **Task**: Design state management patterns for runtime mapping
- **Deliverable**: data-model.md with entity relationships

### 1.2 API Contract Design
- **Task**: Define API endpoints for display mapping operations
- **Task**: Design request/response schemas for ordinal reference operations
- **Deliverable**: contracts/ with OpenAPI specifications

### 1.3 Implementation Design
- **Task**: Design AI agent enhancement for ordinal reference recognition
- **Task**: Plan runtime mapping maintenance and synchronization
- **Task**: Create quickstart guide for developers
- **Deliverable**: quickstart.md with setup instructions

## Phase 2: Agent Responsibilities Design

### 2.1 Conversation Understanding Agent Enhancement
- **Conversation Understanding Agent**: Parse natural language commands for ordinal references
- **Responsibility**: Detect user intent (LIST, EDIT, COMPLETE, UNCOMPLETE, DELETE)
- **Responsibility**: Extract ordinal references (task 1, first task, second task)

### 2.2 Ordinal Resolution Agent Implementation
- **Ordinal Resolution Agent**: Normalize ordinal words and numbers into integers
- **Responsibility**: Handle variations: "task one", "1st task", "second", "task 2"
- **Responsibility**: Validate index range against current task list

### 2.3 Task Mapping Agent Implementation
- **Task Mapping Agent**: Maintain runtime mapping: display_index → task_id
- **Responsibility**: Ensure mapping updates on list, add, delete actions
- **Responsibility**: Provide task_id to execution layer

### 2.4 Action Execution Agent Enhancement
- **Action Execution Agent**: Execute CRUD actions strictly using task_id
- **Responsibility**: Toggle completed / uncompleted status
- **Responsibility**: Trigger edit flow when content is missing

### 2.5 State Consistency Agent Implementation
- **State Consistency Agent**: Keep UI, memory, and storage in sync
- **Responsibility**: Prevent duplicate or ghost tasks
- **Responsibility**: Ensure atomic updates

### 2.6 Feedback & Recovery Agent Enhancement
- **Feedback & Recovery Agent**: Generate confident, user-friendly responses
- **Responsibility**: Handle invalid indexes gracefully
- **Responsibility**: Avoid generic fallback responses when intent is clear

## Phase 3: Skill Integration Planning

### 3.1 Natural Language Processing Skills
- **Skill**: Apply natural language intent classification to ordinal references
- **Skill**: Apply ordinal number extraction & normalization patterns
- **Skill**: Apply validation & error recovery for ambiguous inputs

### 3.2 Runtime State Management Skills
- **Skill**: Apply runtime state mapping for display_index → task_id
- **Skill**: Apply CRUD operation orchestration through mapping layer
- **Skill**: Apply AI agent coordination between specialized agents

## Phase 4: Implementation Planning

### 4.1 Sequential Implementation Phases
1. **Implement Display Mapping**: Create runtime mapping system between display_index and task_id
2. **Enhance AI Parsing**: Update AI agent to recognize ordinal references
3. **Update Task Operations**: Modify CRUD operations to use display mapping
4. **Add Validation**: Implement error handling for invalid indices
5. **Test Integration**: Verify all ordinal reference commands work correctly

### 4.2 Success Criteria Verification
- **Metric**: 95% of ordinal task references (e.g., "task 1 is complete") correctly resolve to intended tasks
- **Metric**: 95% of edit commands using ordinal references (e.g., "edit task 2") successfully update correct tasks
- **Metric**: 95% of completion toggle commands using ordinal references work correctly
- **Metric**: Error response time for invalid task references is under 1 second
- **Metric**: AI agent provides helpful error messages instead of "I'm not sure" responses with 90% confidence
- **Metric**: System handles duplicate task titles correctly when using ordinal references with 95% accuracy
