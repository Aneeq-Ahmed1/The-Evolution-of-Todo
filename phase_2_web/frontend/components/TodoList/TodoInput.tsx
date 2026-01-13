// frontend/components/TodoList/TodoInput.tsx
'use client';

import React, { useState } from 'react';
import Input from '../UI/Input';
import Button from '../UI/Button';

interface TodoInputProps {
  onAdd: (title: string) => void;
}

const TodoInput: React.FC<TodoInputProps> = ({ onAdd }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onAdd(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex space-x-2 mb-6">
      <Input
        type="text"
        placeholder="Add a new todo..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        className="flex-1 h-11 px-3 rounded-lg border border-gray-200 focus:ring-1 focus:ring-gray-400 focus:border-gray-400 shadow-sm"
        aria-label="Add a new todo"
      />
      <Button
        type="submit"
        variant="secondary"
        className="h-11 px-4 rounded-lg transition-transform hover:scale-105 text-gray-700"
      >
        Add
      </Button>
    </form>
  );
};

export default TodoInput;