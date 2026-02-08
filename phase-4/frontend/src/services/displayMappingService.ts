/**
 * Display Mapping Service for AI Task Display Mapping Feature
 *
 * This service manages the runtime mapping between display indices (user-facing)
 * and internal task IDs (database). It maintains state and provides utilities
 * for generating, updating, and querying the mapping.
 */

import { Task } from '../types/task';
import {
  DisplayMapping,
  DisplayMappingState,
  MappingRefreshResponse,
  RefreshMappingRequest
} from '../types/mapping';

/**
 * In-memory storage for display mapping state per user session
 */
let currentMappingState: DisplayMappingState | null = null;

/**
 * Generate display mapping from a list of tasks
 *
 * Assigns sequential 1-based display indices to tasks in order.
 *
 * @param tasks - Array of tasks to map
 * @param userId - User identifier for the mapping
 * @returns Display mapping state object
 *
 * @example
 * const tasks = [
 *   { id: 'task-uuid-1', title: 'Buy groceries', completed: false },
 *   { id: 'task-uuid-2', title: 'Pay bills', completed: true }
 * ];
 * const mapping = generateDisplayMapping(tasks, 'user-123');
 * // mapping.mappings = [
 * //   { display_index: 1, task_id: 'task-uuid-1' },
 * //   { display_index: 2, task_id: 'task-uuid-2' }
 * // ]
 */
export function generateDisplayMapping(
  tasks: Task[],
  userId: string | number
): DisplayMappingState {
  const mappings: DisplayMapping[] = tasks.map((task, index) => ({
    display_index: index + 1, // 1-based indexing
    task_id: task.id
  }));

  const state: DisplayMappingState = {
    mappings,
    user_id: userId,
    last_updated: new Date(),
    isValid: true
  };

  // Store in memory for current session
  currentMappingState = state;

  return state;
}

/**
 * Get current display mapping state
 *
 * @returns Current mapping state or null if not initialized
 */
export function getCurrentMapping(): DisplayMappingState | null {
  return currentMappingState;
}

/**
 * Resolve display index to task ID
 *
 * @param displayIndex - Display index to resolve (1-based)
 * @returns Task ID if found, null otherwise
 *
 * @example
 * const taskId = resolveDisplayIndex(1);
 * // Returns: 'task-uuid-1' (for first displayed task)
 */
export function resolveDisplayIndex(displayIndex: number): string | number | null {
  if (!currentMappingState || displayIndex < 1) {
    return null;
  }

  const mapping = currentMappingState.mappings.find(
    m => m.display_index === displayIndex
  );

  return mapping ? mapping.task_id : null;
}

/**
 * Get display index for a task ID
 *
 * @param taskId - Task ID to find
 * @returns Display index if found, null otherwise
 *
 * @example
 * const displayIndex = getDisplayIndexForTask('task-uuid-1');
 * // Returns: 1 (if this is the first displayed task)
 */
export function getDisplayIndexForTask(taskId: string | number): number | null {
  if (!currentMappingState) {
    return null;
  }

  const mapping = currentMappingState.mappings.find(
    m => m.task_id === taskId
  );

  return mapping ? mapping.display_index : null;
}

/**
 * Update display mapping when task list changes
 *
 * Call this after tasks are added, deleted, or reordered.
 *
 * @param newTasks - Updated list of tasks
 * @param userId - User identifier
 * @returns Updated mapping state
 */
export function refreshDisplayMapping(
  newTasks: Task[],
  userId: string | number
): DisplayMappingState {
  return generateDisplayMapping(newTasks, userId);
}

/**
 * Validate that a display index exists in current mapping
 *
 * @param displayIndex - Display index to validate (1-based)
 * @returns True if display index exists, false otherwise
 *
 * @example
 * if (validateDisplayIndex(5)) {
 *   // Display index 5 exists in current task list
 * } else {
 *   // Display index 5 is out of range
 * }
 */
export function validateDisplayIndex(displayIndex: number): boolean {
  if (!currentMappingState || displayIndex < 1) {
    return false;
  }

  return displayIndex <= currentMappingState.mappings.length;
}

/**
 * Get total number of tasks in current mapping
 *
 * @returns Number of tasks or 0 if no mapping exists
 */
export function getTotalTasks(): number {
  return currentMappingState ? currentMappingState.mappings.length : 0;
}

/**
 * Get all display indices
 *
 * @returns Array of valid display indices (1-based)
 *
 * @example
 * const indices = getAllDisplayIndices();
 * // Returns: [1, 2, 3, 4, 5] (if 5 tasks exist)
 */
export function getAllDisplayIndices(): number[] {
  if (!currentMappingState) {
    return [];
  }

  return currentMappingState.mappings.map(m => m.display_index);
}

/**
 * Clear current display mapping
 *
 * Call this when user logs out or session ends.
 */
export function clearDisplayMapping(): void {
  currentMappingState = null;
}

/**
 * Check if display mapping is valid and up-to-date
 *
 * @returns True if mapping exists and is valid, false otherwise
 */
export function isMappingValid(): boolean {
  return currentMappingState !== null && currentMappingState.isValid;
}

/**
 * Invalidate current display mapping
 *
 * Marks the current mapping as invalid without clearing it.
 * Use this when you know the task list has changed but haven't refreshed yet.
 */
export function invalidateMapping(): void {
  if (currentMappingState) {
    currentMappingState.isValid = false;
  }
}
