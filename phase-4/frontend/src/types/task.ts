export type Priority = 'low' | 'medium' | 'high';
export type RecurrencePattern = 'daily' | 'weekly' | 'monthly';

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;

  // Intermediate Level
  priority: Priority;
  tags?: string; // Comma-separated tags
  category?: string;

  // Advanced Level
  due_date?: string; // ISO date string
  due_time?: string; // HH:MM format
  is_recurring: boolean;
  recurrence_pattern?: RecurrencePattern;
  recurrence_interval?: number;
  next_occurrence?: string; // ISO date string
}

export interface TaskWithDisplayIndex extends Task {
  display_index: number;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  completed?: boolean;

  // Intermediate
  priority?: Priority;
  tags?: string;
  category?: string;

  // Advanced
  due_date?: string;
  due_time?: string;
  is_recurring?: boolean;
  recurrence_pattern?: RecurrencePattern;
  recurrence_interval?: number;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;

  // Intermediate
  priority?: Priority;
  tags?: string;
  category?: string;

  // Advanced
  due_date?: string;
  due_time?: string;
  is_recurring?: boolean;
  recurrence_pattern?: RecurrencePattern;
  recurrence_interval?: number;
}

export interface TaskFilters {
  search?: string;
  priority?: Priority | 'all';
  category?: string | 'all';
  completed?: boolean | 'all';
  sortBy?: 'created_at' | 'due_date' | 'priority' | 'title';
  sortOrder?: 'asc' | 'desc';
}
