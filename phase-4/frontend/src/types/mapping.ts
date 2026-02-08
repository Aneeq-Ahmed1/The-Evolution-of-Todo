/**
 * Display Mapping Types for AI Task Display Mapping Feature
 *
 * These types support the runtime mapping between display indices (user-facing)
 * and internal task IDs (database).
 */

/**
 * Single display mapping entry linking a display index to a task ID
 */
export interface DisplayMapping {
  display_index: number;  // 1-based sequential index shown to user
  task_id: string | number;  // Internal task identifier
}

/**
 * Complete display mapping state for a user session
 */
export interface DisplayMappingState {
  mappings: DisplayMapping[];
  user_id: string | number;
  last_updated: Date;
  isValid: boolean;
}

/**
 * Response from mapping refresh endpoint
 */
export interface MappingRefreshResponse {
  mapping_updated: boolean;
  total_mappings: number;
  display_mapping: DisplayMapping[];
  refreshed_at: string;  // ISO 8601 timestamp
}

/**
 * Request to resolve display index to task ID
 */
export interface ResolveDisplayIndexRequest {
  display_index: number;
  user_id: string | number;
}

/**
 * Response from display index resolution
 */
export interface ResolveDisplayIndexResponse {
  task_id: string | number;
  display_index: number;
  valid: boolean;
  error?: string;
}

/**
 * Request to refresh display mapping
 */
export interface RefreshMappingRequest {
  user_id: string | number;
  tasks: Array<{
    id: string | number;
    title: string;
    completed: boolean;
  }>;
}
