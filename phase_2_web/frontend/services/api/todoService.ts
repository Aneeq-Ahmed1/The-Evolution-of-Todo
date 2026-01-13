// frontend/services/api/todoService.ts
import { TodoItem } from '../types';
import { apiClient } from './apiClient';

// Helper function to get user ID from localStorage
const getCurrentUserId = (): string => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser);
      return user.id;
    } catch (e) {
      console.error('Error parsing user from localStorage', e);
      throw new Error('Could not get user ID');
    }
  }
  throw new Error('User not authenticated');
};

export const todoService = {
  async getAllTodos(): Promise<TodoItem[]> {
    const userId = getCurrentUserId();
    const response = await apiClient.request(`/api/${userId}/tasks`);
    return response.map((todo: any) => ({
      ...todo,
      createdAt: new Date(todo.created_at || todo.createdAt),
      updatedAt: todo.updated_at ? new Date(todo.updated_at) : undefined
    }));
  },

  async createTodo(title: string, description?: string): Promise<TodoItem> {
    const userId = getCurrentUserId();
    const response = await apiClient.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
    return {
      ...response,
      createdAt: new Date(response.created_at || response.createdAt),
      updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
    };
  },

  async updateTodo(id: string, updates: Partial<TodoItem>): Promise<TodoItem> {
    const userId = getCurrentUserId();
    const response = await apiClient.request(`/api/${userId}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
    return {
      ...response,
      id,
      createdAt: new Date(response.created_at || response.createdAt),
      updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
    };
  },

  async deleteTodo(id: string): Promise<void> {
    const userId = getCurrentUserId();
    await apiClient.request(`/api/${userId}/tasks/${id}`, {
      method: 'DELETE',
    });
  },

  async toggleTodoCompletion(id: string): Promise<TodoItem> {
    const userId = getCurrentUserId();
    const response = await apiClient.request(`/api/${userId}/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({}), // Backend toggles the completion status without needing explicit value
    });
    return {
      ...response,
      id,
      createdAt: new Date(response.created_at || response.createdAt),
      updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
    };
  },
};