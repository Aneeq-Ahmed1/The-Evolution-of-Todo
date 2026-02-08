import React, { useState, useEffect } from 'react';
import { Task, TaskWithDisplayIndex } from '../types/task';
import { apiClient } from '../lib/api';
import TaskItem from './TaskItem';
import { validateDisplayIndex, getTotalTasks } from '../services/displayMappingService';

interface TaskListProps {
  tasks: (Task | TaskWithDisplayIndex)[];
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: number) => void;
  onTaskEdit?: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdate, onTaskDelete, onTaskEdit }) => {

  const handleTaskToggle = async (task: Task) => {
    try {
      const updatedTask = await apiClient.tasks.updateStatus(task.id.toString(), !task.completed);
      onTaskUpdate?.(updatedTask.data);
    } catch (err) {
      console.error('Error updating task:', err);
      alert('Failed to update task status.');
    }
  };

  const handleTaskDelete = async (taskId: number) => {
    try {
      console.log('Attempting to delete task with ID:', taskId);
      const response = await apiClient.tasks.delete(taskId.toString());
      console.log('Delete response:', response);
      onTaskDelete?.(taskId);
      console.log('Task successfully deleted from UI');
    } catch (err) {
      console.error('Error deleting task:', err);
      // Provide more detailed error information
      if (err instanceof Error) {
        console.error('Error message:', err.message);
        alert(`Failed to delete task: ${err.message}`);
      } else {
        alert('Failed to delete task. Please check console for details.');
      }
    }
  };

  if (tasks.length === 0) {
    return <div className="text-center py-4">No tasks found. Add a new task to get started!</div>;
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={handleTaskToggle}
            onDelete={handleTaskDelete}
            onEdit={onTaskEdit}
          />
        ))}
      </ul>
    </div>
  );
};

export default TaskList;