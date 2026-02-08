// frontend/services/api/todoService.ts
import { TodoItem } from '../types';
import { apiClient } from './apiClient';

// Helper function to get user ID from localStorage
const getCurrentUserId = (): string => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser);
      if (user && user.id) {
        return user.id;
      } else {
        throw new Error('User ID not found in stored user data');
      }
    } catch (e) {
      console.error('Error parsing user from localStorage', e);
      throw new Error('Could not get user ID');
    }
  }
  throw new Error('User not authenticated');
};

// Helper function to check if user is authenticated
const isUserAuthenticated = (): boolean => {
  const storedUser = localStorage.getItem('user');
  const token = localStorage.getItem('token');
  return !!storedUser && !!token;
};

export const todoService = {
  async getAllTodos(): Promise<TodoItem[]> {
    if (!isUserAuthenticated()) {
      console.error('User not authenticated when trying to fetch todos');
      throw new Error('User not authenticated');
    }

    try {
      const userId = getCurrentUserId();
      console.log(`Attempting to fetch todos for user ID: ${userId}`);

      const response = await apiClient.request(`/api/${userId}/tasks`);
      console.log(`Successfully fetched ${response.length} todos for user ID: ${userId}`);

      return response.map((todo: any) => ({
        ...todo,
        createdAt: new Date(todo.created_at || todo.createdAt),
        updatedAt: todo.updated_at ? new Date(todo.updated_at) : undefined
      }));
    } catch (error) {
      console.error('Error in getAllTodos:', error);
      throw error;
    }
  },

  async createTodo(title: string, description?: string): Promise<TodoItem> {
    if (!isUserAuthenticated()) {
      console.error('User not authenticated when trying to create todo');
      throw new Error('User not authenticated');
    }

    try {
      const userId = getCurrentUserId();
      console.log(`Attempting to create todo for user ID: ${userId}`, { title, description });

      const response = await apiClient.request(`/api/${userId}/tasks`, {
        method: 'POST',
        body: JSON.stringify({ title, description }),
      });

      console.log('Successfully created todo:', response);
      return {
        ...response,
        createdAt: new Date(response.created_at || response.createdAt),
        updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
      };
    } catch (error) {
      console.error('Error in createTodo:', error);
      throw error;
    }
  },

  async updateTodo(id: string, updates: Partial<TodoItem>): Promise<TodoItem> {
    if (!isUserAuthenticated()) {
      console.error('User not authenticated when trying to update todo');
      throw new Error('User not authenticated');
    }

    try {
      const userId = getCurrentUserId();
      console.log(`Attempting to update todo ID: ${id} for user ID: ${userId}`, updates);

      const response = await apiClient.request(`/api/${userId}/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify(updates),
      });

      console.log('Successfully updated todo:', response);
      return {
        ...response,
        id,
        createdAt: new Date(response.created_at || response.createdAt),
        updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
      };
    } catch (error) {
      console.error('Error in updateTodo:', error);
      throw error;
    }
  },

  async deleteTodo(id: string): Promise<void> {
    if (!isUserAuthenticated()) {
      console.error('User not authenticated when trying to delete todo');
      throw new Error('User not authenticated');
    }

    try {
      const userId = getCurrentUserId();
      console.log(`Attempting to delete todo ID: ${id} for user ID: ${userId}`);

      await apiClient.request(`/api/${userId}/tasks/${id}`, {
        method: 'DELETE',
      });

      console.log('Successfully deleted todo ID:', id);
    } catch (error) {
      console.error('Error in deleteTodo:', error);
      throw error;
    }
  },

  async toggleTodoCompletion(id: string): Promise<TodoItem> {
    if (!isUserAuthenticated()) {
      console.error('User not authenticated when trying to toggle todo completion');
      throw new Error('User not authenticated');
    }

    try {
      const userId = getCurrentUserId();
      console.log(`Attempting to toggle completion for todo ID: ${id} for user ID: ${userId}`);

      const response = await apiClient.request(`/api/${userId}/tasks/${id}/complete`, {
        method: 'PATCH',
        body: JSON.stringify({}), // Backend toggles the completion status without needing explicit value
      });

      console.log('Successfully toggled todo completion:', response);
      return {
        ...response,
        id,
        createdAt: new Date(response.created_at || response.createdAt),
        updatedAt: response.updated_at ? new Date(response.updated_at) : undefined
      };
    } catch (error) {
      console.error('Error in toggleTodoCompletion:', error);
      throw error;
    }
  },
};