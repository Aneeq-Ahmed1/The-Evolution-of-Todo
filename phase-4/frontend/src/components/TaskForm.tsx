import React, { useState } from 'react';
import { Task, Priority, RecurrencePattern } from '../types/task';
import { apiClient } from '../lib/api';

interface TaskFormProps {
  task?: Task;
  onSuccess?: (task: Task) => void;
  onCancel?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSuccess, onCancel }) => {
  // Basic fields
  const [title, setTitle] = useState<string>(task?.title || '');
  const [description, setDescription] = useState<string>(task?.description || '');

  // Intermediate fields
  const [priority, setPriority] = useState<Priority>(task?.priority || 'medium');
  const [category, setCategory] = useState<string>(task?.category || '');
  const [tags, setTags] = useState<string>(task?.tags || '');

  // Advanced fields
  const [dueDate, setDueDate] = useState<string>(task?.due_date?.split('T')[0] || '');
  const [dueTime, setDueTime] = useState<string>(task?.due_time || '');
  const [isRecurring, setIsRecurring] = useState<boolean>(task?.is_recurring || false);
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern>(task?.recurrence_pattern || 'daily');
  const [recurrenceInterval, setRecurrenceInterval] = useState<number>(task?.recurrence_interval || 1);

  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const isEditing = !!task;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const taskData = {
        title,
        description: description, // Send empty string if cleared
        priority,
        category: category, // Send empty string if cleared
        tags: tags, // Send empty string if cleared
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
        due_time: dueTime,
        is_recurring: isRecurring,
        recurrence_pattern: isRecurring ? recurrencePattern : null,
        recurrence_interval: isRecurring ? recurrenceInterval : null,
      };

      if (isEditing) {
        const response = await apiClient.tasks.update(task.id.toString(), taskData);
        onSuccess?.(response.data);
      } else {
        const response = await apiClient.tasks.create(taskData);
        onSuccess?.(response.data);
      }

      if (!isEditing) {
        // Reset form
        setTitle('');
        setDescription('');
        setPriority('medium');
        setCategory('');
        setTags('');
        setDueDate('');
        setDueTime('');
        setIsRecurring(false);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to save task');
      console.error('Error saving task:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded p-4" style={{ border: '1px solid #e0e4e9' }}>
      <h3 className="text-base font-semibold mb-4" style={{ color: '#232a31' }}>
        {isEditing ? 'Edit Task' : 'Create New Task'}
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 rounded" style={{ backgroundColor: '#fee', border: '1px solid #fcc' }}>
            <p className="text-sm" style={{ color: '#c00' }}>{error}</p>
          </div>
        )}

        {/* Title */}
        <div>
          <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
            Title <span style={{ color: '#c00' }}>*</span>
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full px-3 py-2.5 rounded text-sm"
            style={{ border: '1px solid #e0e4e9' }}
            placeholder="What needs to be done?"
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
            Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2.5 rounded text-sm"
            style={{ border: '1px solid #e0e4e9' }}
            placeholder="Add more details (optional)"
          />
        </div>

        {/* Priority & Category - Row */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
              Priority
            </label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as Priority)}
              className="w-full px-3 py-2.5 rounded text-sm"
              style={{ border: '1px solid #e0e4e9' }}
            >
              <option value="low">🟢 Low</option>
              <option value="medium">🟡 Medium</option>
              <option value="high">🔴 High</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
              Category
            </label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2.5 rounded text-sm"
              style={{ border: '1px solid #e0e4e9' }}
              placeholder="work, personal, etc."
            />
          </div>
        </div>

        {/* Tags */}
        <div>
          <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
            Tags <span className="text-xs" style={{ color: '#828a93' }}>(comma-separated)</span>
          </label>
          <input
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            className="w-full px-3 py-2.5 rounded text-sm"
            style={{ border: '1px solid #e0e4e9' }}
            placeholder="urgent, meeting, important"
          />
        </div>

        {/* Due Date & Time - Row */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
              Due Date
            </label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-3 py-2.5 rounded text-sm"
              style={{ border: '1px solid #e0e4e9' }}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
              Due Time
            </label>
            <input
              type="time"
              value={dueTime}
              onChange={(e) => setDueTime(e.target.value)}
              className="w-full px-3 py-2.5 rounded text-sm"
              style={{ border: '1px solid #e0e4e9' }}
            />
          </div>
        </div>

        {/* Recurring Task Checkbox */}
        <div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={isRecurring}
              onChange={(e) => setIsRecurring(e.target.checked)}
              className="w-4 h-4 rounded"
              style={{ accentColor: '#7e1fff' }}
            />
            <span className="text-sm font-medium" style={{ color: '#232a31' }}>
              🔁 Recurring Task
            </span>
          </label>
        </div>

        {/* Recurring Options - Show only if recurring */}
        {isRecurring && (
          <div className="p-3 rounded space-y-3" style={{ backgroundColor: '#f5f8fa', border: '1px solid #e0e4e9' }}>
            <p className="text-xs font-medium" style={{ color: '#232a31' }}>Recurrence Settings</p>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium mb-1" style={{ color: '#232a31' }}>
                  Repeat Every
                </label>
                <input
                  type="number"
                  min="1"
                  value={recurrenceInterval}
                  onChange={(e) => setRecurrenceInterval(Number(e.target.value))}
                  className="w-full px-2 py-1.5 rounded text-sm"
                  style={{ border: '1px solid #e0e4e9' }}
                />
              </div>

              <div>
                <label className="block text-xs font-medium mb-1" style={{ color: '#232a31' }}>
                  Pattern
                </label>
                <select
                  value={recurrencePattern}
                  onChange={(e) => setRecurrencePattern(e.target.value as RecurrencePattern)}
                  className="w-full px-2 py-1.5 rounded text-sm"
                  style={{ border: '1px solid #e0e4e9' }}
                >
                  <option value="daily">Day(s)</option>
                  <option value="weekly">Week(s)</option>
                  <option value="monthly">Month(s)</option>
                </select>
              </div>
            </div>

            <p className="text-xs" style={{ color: '#6e7780' }}>
              Task will repeat every {recurrenceInterval} {recurrencePattern === 'daily' ? 'day(s)' : recurrencePattern === 'weekly' ? 'week(s)' : 'month(s)'}
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end gap-2 pt-2">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 rounded text-sm"
              style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
            style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
          >
            {isSubmitting ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Task' : 'Create Task')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;
