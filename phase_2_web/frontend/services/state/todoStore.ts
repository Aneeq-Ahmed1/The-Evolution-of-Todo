// frontend/services/state/todoStore.ts
import { useState, useEffect } from 'react';
import { TodoItem, TodoList } from '../types';
import { todoService } from '../api/todoService';

export const useTodoStore = () => {
  const [todoList, setTodoList] = useState<TodoList>({
    items: [],
    filter: 'all',
    isLoading: false,
    error: undefined,
  });

  // Load todos on mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setTodoList(prev => ({ ...prev, isLoading: true, error: undefined }));
      const todos = await todoService.getAllTodos();
      setTodoList(prev => ({
        ...prev,
        items: todos,
        isLoading: false,
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        isLoading: false,
        error: (error as Error).message,
      }));
    }
  };

  const addTodo = async (title: string) => {
    try {
      const newTodo = await todoService.createTodo(title);
      setTodoList(prev => ({
        ...prev,
        items: [...prev.items, newTodo],
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        error: (error as Error).message,
      }));
    }
  };

  const toggleTodo = async (id: string) => {
    try {
      const updatedTodo = await todoService.toggleTodoCompletion(id);
      setTodoList(prev => ({
        ...prev,
        items: prev.items.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        error: (error as Error).message,
      }));
    }
  };

  const updateTodo = async (id: string, updates: Partial<TodoItem>) => {
    try {
      const updatedTodo = await todoService.updateTodo(id, updates);
      setTodoList(prev => ({
        ...prev,
        items: prev.items.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        error: (error as Error).message,
      }));
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await todoService.deleteTodo(id);
      setTodoList(prev => ({
        ...prev,
        items: prev.items.filter(todo => todo.id !== id),
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        error: (error as Error).message,
      }));
    }
  };

  const setFilter = (filter: 'all' | 'active' | 'completed') => {
    setTodoList(prev => ({ ...prev, filter }));
  };

  const updateTodoTitle = async (id: string, title: string) => {
    try {
      const updatedTodo = await todoService.updateTodo(id, { title });
      setTodoList(prev => ({
        ...prev,
        items: prev.items.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
      }));
    } catch (error) {
      setTodoList(prev => ({
        ...prev,
        error: (error as Error).message,
      }));
    }
  };

  return {
    todoList,
    fetchTodos,
    addTodo,
    toggleTodo,
    updateTodo,
    updateTodoTitle,
    deleteTodo,
    setFilter,
  };
};