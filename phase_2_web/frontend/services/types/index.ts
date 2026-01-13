// frontend/services/types/index.ts
export interface TodoItem {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  updatedAt?: Date;
}

export interface TodoList {
  items: TodoItem[];
  filter: 'all' | 'active' | 'completed';
  isLoading: boolean;
  error?: string;
}

export interface UIState {
  isLoading: boolean;
  error?: string;
  isEmpty: boolean;
  isAuthenticated: boolean;
}

export interface AuthCredentials {
  email: string;
  password: string;
  name?: string;
}

export interface FormState {
  isSubmitting: boolean;
  errors: Record<string, string>;
  success: boolean;
}