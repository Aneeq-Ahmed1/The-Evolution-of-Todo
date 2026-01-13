// frontend/components/TodoList/TodoItem.tsx
'use client';

import React, { useState } from 'react';
import Button from '../UI/Button';
import Input from '../UI/Input';

interface TodoItemProps {
  id: string;
  title: string;
  completed: boolean;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit?: (id: string, title: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  id,
  title,
  completed,
  onToggle,
  onDelete,
  onEdit
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);

  const handleToggle = () => {
    onToggle(id);
  };

  const handleDelete = () => {
    onDelete(id);
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(title);
  };

  const handleSave = () => {
    if (editTitle.trim() && onEdit) {
      onEdit(id, editTitle.trim());
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(title);
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  return (
    <div className={`flex items-center justify-between p-3 border-b border-gray-100 transition-all duration-200 ease-in-out hover:bg-gray-50 ${completed ? 'bg-gray-50' : 'bg-white'}`}>
      <div className="flex items-center space-x-3 flex-1">
        <input
          type="checkbox"
          checked={completed}
          onChange={handleToggle}
          className="h-5 w-5 rounded border-gray-300 text-gray-600 focus:ring-gray-500 cursor-pointer transition-all duration-150"
          aria-label={completed ? `Mark ${title} as incomplete` : `Mark ${title} as complete`}
        />
        {isEditing ? (
          <div className="flex-1 flex space-x-2">
            <Input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 text-base"
              autoFocus
            />
            <div className="flex space-x-1">
              <Button
                variant="primary"
                size="sm"
                onClick={handleSave}
                className="px-2 py-1 text-xs"
              >
                Save
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={handleCancel}
                className="px-2 py-1 text-xs"
              >
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex justify-between items-center">
            <span
              className={`text-base transition-all duration-200 ${completed ? 'line-through text-gray-500' : 'text-gray-700'} cursor-pointer`}
              onClick={handleEdit}
            >
              {title}
            </span>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleEdit}
              className="ml-2 transition-all duration-200 ease-in-out hover:scale-105 text-gray-500 hover:text-gray-700 hover:bg-gray-200"
            >
              Edit
            </Button>
          </div>
        )}
      </div>
      <div className="flex space-x-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={handleDelete}
          className="transition-all duration-200 ease-in-out hover:scale-105 text-gray-500 hover:text-gray-700 hover:bg-gray-200"
        >
          Delete
        </Button>
      </div>
    </div>
  );
};

export default TodoItem;