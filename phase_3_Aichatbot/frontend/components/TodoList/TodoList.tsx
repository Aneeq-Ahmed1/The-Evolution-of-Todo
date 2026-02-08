// frontend/components/TodoList/TodoList.tsx
'use client';

import React from 'react';
import { useTodoStore } from '../../services/state/todoStore';
import TodoItem from './TodoItem';
import TodoInput from './TodoInput';
import { TodoItem as TodoItemType } from '../../services/types';

const TodoList: React.FC = () => {
  const { todoList, toggleTodo, deleteTodo, addTodo, setFilter, updateTodoTitle } = useTodoStore();

  const filteredTodos = todoList.items.filter(todo => {
    if (todoList.filter === 'active') return !todo.completed;
    if (todoList.filter === 'completed') return todo.completed;
    return true;
  });

  const handleAddTodo = (title: string) => {
    addTodo(title);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-3xl font-medium text-gray-800 mb-1">My Todos</h1>
        <p className="text-gray-500">Stay organized and get things done</p>
      </div>

      {/* Add Todo Form */}
      <TodoInput onAdd={handleAddTodo} />

      {/* Filter Buttons */}
      <div className="flex space-x-2 mb-4">
        {(['all', 'active', 'completed'] as const).map(filter => (
          <button
            key={filter}
            className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
              todoList.filter === filter
                ? 'bg-gray-800 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={() => setFilter(filter)}
          >
            {filter.charAt(0).toUpperCase() + filter.slice(1)}
          </button>
        ))}
      </div>

      {/* Loading State */}
      {todoList.isLoading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading todos...</p>
        </div>
      )}

      {/* Error State */}
      {todoList.error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          Error: {todoList.error}
        </div>
      )}

      {/* Empty State */}
      {!todoList.isLoading && !todoList.error && filteredTodos.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">No todos yet</div>
          <p className="text-gray-600">Add a new todo to get started</p>
        </div>
      )}

      {/* Todo List */}
      {!todoList.isLoading && !todoList.error && filteredTodos.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {filteredTodos.map(todo => (
            <div
              key={todo.id}
              className="animate-fadeIn"
            >
              <TodoItem
                id={todo.id}
                title={todo.title}
                completed={todo.completed}
                onToggle={toggleTodo}
                onDelete={deleteTodo}
                onEdit={updateTodoTitle}
              />
            </div>
          ))}
        </div>
      )}

      {/* Summary */}
      {!todoList.isLoading && !todoList.error && todoList.items.length > 0 && (
        <div className="mt-4 text-center text-gray-600">
          {todoList.items.filter(t => !t.completed).length} items remaining
        </div>
      )}
    </div>
  );
};

export default TodoList;