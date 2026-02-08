# Research: AI Task Display Mapping

**Feature**: 001-ai-task-mapping
**Date**: 2026-01-04
**Status**: Complete

## Research Objectives

This research document analyzes the current state of the AI Agent based Todo Application to identify root causes of why ordinal task references (e.g., "task 1 is complete", "edit task 2") are not working, and provides recommendations for implementation.

## Current State Analysis

### Existing Architecture
- **Frontend**: Next.js 15 application with task management UI
- **Backend**: FastAPI with SQLModel ORM and Neon PostgreSQL
- **AI Agent**: Connected and responding to user requests
- **Task Display**: Tasks shown with sequential numbers (1, 2, 3, etc.)

### Identified Issues
1. **Task Number Mapping**: Displayed task numbers (1,2,3) are not mapped to internal task_id
2. **Ordinal Reference Recognition**: AI does not understand ordinal references like "task 1", "first task"
3. **Intent Parsing**: Current intent parser does not handle display_index to task_id resolution
4. **Runtime Mapping**: No mechanism to maintain display_index → task_id mapping
5. **Error Handling**: Generic fallback responses instead of helpful error messages
6. **Index Validation**: No validation for out-of-range task numbers

## Root Cause Analysis

### Backend Issues
- Task listing assigns display numbers but doesn't maintain mapping to internal task_id
- API endpoints accept only internal task_id, not display_index
- No mechanism to convert display_index to task_id before backend operations

### Frontend Issues
- Task display shows numbered list but doesn't expose mapping to AI agent
- No coordination between display numbers and internal task IDs
- State management doesn't track display_index → task_id relationship

### AI Agent Issues
- Natural language processing doesn't recognize ordinal task references
- Intent mapping doesn't include display_index to task_id resolution
- No validation of whether referenced task number exists in current view

## Recommended Approach

### 1. Runtime Mapping Implementation
- Create a runtime mapping between display_index and internal task_id
- Maintain mapping per user session for current task view
- Refresh mapping when task list changes (add/delete/reorder)

### 2. AI Intent Enhancement
- Update natural language processing to recognize ordinal references
- Implement display_index extraction from user commands
- Add validation to ensure referenced task exists in current mapping

### 3. Resolution Logic
- Convert display_index to task_id before backend API calls
- Execute operations using internal task_id for consistency
- Provide helpful error messages for invalid indices

### 4. State Management
- Maintain display mapping in both frontend and AI agent context
- Update mapping when task list changes
- Ensure UI and AI agent have synchronized task numbering

## Technology Considerations

### Best Practices for Display Mapping
- **Runtime Mapping**: Store display_index → task_id mapping in memory per session
- **Ordinal Recognition**: Use regex patterns to identify ordinal references in text
- **Error Handling**: Provide specific error messages for invalid task numbers
- **Index Validation**: Validate display_index exists before attempting resolution

### State Management Patterns
- **Synchronization**: Keep display mapping consistent between UI and AI context
- **Atomic Updates**: Update mapping when task list changes to prevent inconsistencies
- **Performance**: Efficient lookup for display_index → task_id conversion

## Implementation Recommendations

### Phase 1: Core Mapping
1. Implement runtime display_index → task_id mapping
2. Update AI agent to recognize ordinal references
3. Add conversion logic before backend API calls

### Phase 2: Validation & Error Handling
1. Add validation for display_index existence
2. Implement helpful error messages for invalid references
3. Test with various ordinal formats and edge cases

### Phase 3: Integration & Testing
1. Test all ordinal reference commands with real user scenarios
2. Verify mapping stays synchronized with task list changes
3. Ensure error handling works for all edge cases

## Success Metrics

- Ordinal task references (e.g., "task 1 is complete") correctly resolve to intended tasks
- Edit commands using ordinal references (e.g., "edit task 2") work correctly
- Completion toggle commands using ordinal references work properly
- Error response time for invalid task references is under 1 second
- AI agent provides helpful error messages instead of generic fallback responses
- System handles duplicate task titles correctly when using ordinal references