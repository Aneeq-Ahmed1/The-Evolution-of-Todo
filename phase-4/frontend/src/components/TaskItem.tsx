import React, { useState } from 'react';
import { Task, TaskWithDisplayIndex } from '../types/task';

interface TaskItemProps {
  task: Task | TaskWithDisplayIndex;
  onToggle: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onEdit?: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete, onEdit }) => {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const getPriorityStyle = (priority: string) => {
    switch(priority) {
      case 'high': return { bg: '#fee', color: '#c00', text: 'HIGH' };
      case 'medium': return { bg: '#fef3e0', color: '#f59e0b', text: 'MED' };
      case 'low': return { bg: '#efe', color: '#0a0', text: 'LOW' };
      default: return { bg: '#f0f3f5', color: '#6e7780', text: 'MED' };
    }
  };

  const isOverdue = () => {
    if (!task.due_date || task.completed) return false;
    return new Date(task.due_date) < new Date();
  };

  const priorityStyle = getPriorityStyle(task.priority);

  // Check if the task has a display_index property
  const hasDisplayIndex = 'display_index' in task && task.display_index !== undefined;

  return (
    <li className="p-4 hover:bg-gray-50 transition-colors border-b" style={{ borderColor: '#e0e4e9' }}>
      <div className="flex items-start gap-3">
        {/* Display Index Badge */}
        {hasDisplayIndex && (
          <div className="flex items-center justify-center w-6 h-6 rounded-full text-xs font-semibold"
               style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}>
            {task.display_index}
          </div>
        )}

        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggle(task as Task)}
          className="mt-1 w-4 h-4 rounded"
          style={{ accentColor: '#7e1fff' }}
        />

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title & Badges Row */}
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <h3 className={`text-sm font-medium ${task.completed ? 'line-through' : ''}`} style={{ color: task.completed ? '#828a93' : '#232a31' }}>
              {task.title}
            </h3>

            {/* Priority Badge */}
            <span className="px-2 py-0.5 rounded text-xs font-medium" style={{
              backgroundColor: priorityStyle.bg,
              color: priorityStyle.color
            }}>
              {priorityStyle.text}
            </span>

            {/* Category Badge */}
            {task.category && (
              <span className="px-2 py-0.5 rounded text-xs font-medium" style={{
                backgroundColor: '#f0f3f5',
                color: '#6e7780'
              }}>
                {task.category}
              </span>
            )}

            {/* Recurring Icon */}
            {task.is_recurring && (
              <span className="text-xs" style={{ color: '#7e1fff' }}>
                🔁 {task.recurrence_pattern}
              </span>
            )}
          </div>

          {/* Description Box */}
          {task.description && (
            <div className="mt-2 mb-3 p-3 rounded border bg-gray-50/50" style={{ borderColor: '#e0e4e9' }}>
              <span className="block text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#828a93' }}>
                Description
              </span>
              <p className="text-sm leading-relaxed" style={{ color: task.completed ? '#828a93' : '#4a5568' }}>
                {task.description}
              </p>
            </div>
          )}

          {/* Tags */}
          {task.tags && (
            <div className="flex gap-1 flex-wrap mb-2">
              {task.tags.split(',').map((tag, idx) => (
                <span key={idx} className="px-2 py-0.5 rounded text-xs" style={{
                  backgroundColor: '#f0f3f5',
                  color: '#7e1fff'
                }}>
                  #{tag.trim()}
                </span>
              ))}
            </div>
          )}

          {/* Due Date & Time */}
          {task.due_date && (
            <div className="flex items-center gap-2 text-xs mb-1">
              <span style={{ color: isOverdue() ? '#c00' : '#6e7780' }}>
                📅 {new Date(task.due_date).toLocaleDateString()}
                {task.due_time && ` at ${task.due_time}`}
                {isOverdue() && <span className="font-semibold"> (OVERDUE)</span>}
              </span>
            </div>
          )}

          {/* Metadata */}
          <p className="text-xs" style={{ color: '#828a93' }}>
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-1">
          {onEdit && (
            <button
              onClick={() => onEdit(task as Task)}
              className="px-2 py-1 rounded text-xs"
              style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
            >
              Edit
            </button>
          )}
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="px-2 py-1 rounded text-xs"
            style={{ backgroundColor: '#fee', color: '#c00' }}
          >
            Delete
          </button>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded p-6 max-w-sm mx-4" style={{ border: '1px solid #e0e4e9' }}>
            <h3 className="text-base font-semibold mb-2" style={{ color: '#232a31' }}>
              Delete Task?
            </h3>
            <p className="text-sm mb-4" style={{ color: '#6e7780' }}>
              Are you sure you want to delete "{task.title}"? This action cannot be undone.
            </p>
            <div className="flex gap-2 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="px-4 py-2 rounded text-sm"
                style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  onDelete(task.id);
                  setShowDeleteConfirm(false);
                }}
                className="px-4 py-2 rounded text-sm font-medium"
                style={{ backgroundColor: '#c00', color: '#ffffff' }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </li>
  );
};

export default TaskItem;
