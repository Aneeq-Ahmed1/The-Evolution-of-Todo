"use client";

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TaskList from '../../../components/TaskList';
import TaskForm from '../../../components/TaskForm';
import { Task, Priority } from '../../../types/task';
import { apiClient } from '../../../lib/api';
import { signOut } from '../../../lib/auth';
import { generateDisplayMapping, refreshDisplayMapping } from '../../../services/displayMappingService';

const TaskDashboardPage = () => {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Basic filter
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  // Advanced filters
  const [searchTerm, setSearchTerm] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<'all' | Priority>('all');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [sortBy, setSortBy] = useState<'created_at' | 'due_date' | 'priority' | 'title'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const handleLogout = async () => {
    await signOut();
    router.push('/');
  };

  const handleGoHome = () => {
    router.push('/');
  };

  useEffect(() => {
    loadTasks();
  }, [filter, searchTerm, priorityFilter, categoryFilter, sortBy, sortOrder]);

  // Refresh display mapping whenever tasks change
  useEffect(() => {
    if (tasks.length > 0) {
      const userId = localStorage.getItem('user_id') || 'current_user';
      refreshDisplayMapping(tasks, userId);
    }
  }, [tasks]);

  const handleApplyFilters = () => {
    loadTasks();
  };

  const loadTasks = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');

      if (!token) {
        router.push('/auth/login');
        return;
      }

      // Build filters object
      const filters = {
        search: searchTerm || undefined,
        priority: priorityFilter !== 'all' ? priorityFilter : undefined,
        category: categoryFilter || undefined,
        completed: filter === 'all' ? undefined : filter === 'completed',
        sortBy,
        sortOrder
      };

      const response = await apiClient.tasks.getAll(filters);
      setTasks(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Error loading tasks:', err);

      if (err?.status === 401) {
        setError('Session expired. Please login again.');
        setTimeout(() => router.push('/auth/login'), 2000);
      } else if (err?.status === 0) {
        setError('Cannot connect to server. Please check if backend is running.');
      } else {
        setError(err?.message || 'Failed to load tasks.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleFormSubmit = (task: Task) => {
    if (editingTask) {
      setTasks(tasks.map(t => t.id === task.id ? task : t));
    } else {
      setTasks([task, ...tasks]);
    }
    setShowForm(false);
    setEditingTask(null);
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleTaskUpdate = (task: Task) => {
    setTasks(tasks.map(t => t.id === task.id ? task : t));
  };

  const handleTaskDelete = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  // Apply filters to the tasks
  const filteredTasks = tasks.filter(task => {
    // Apply status filter
    if (filter === 'completed' && !task.completed) return false;
    if (filter === 'pending' && task.completed) return false;

    // Apply search term filter
    if (searchTerm && !task.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
        (!task.description || !task.description.toLowerCase().includes(searchTerm.toLowerCase())) &&
        (!task.category || !task.category.toLowerCase().includes(searchTerm.toLowerCase()))) {
      return false;
    }

    // Apply priority filter
    if (priorityFilter !== 'all' && task.priority !== priorityFilter) return false;

    // Apply category filter
    if (categoryFilter && (!task.category || !task.category.toLowerCase().includes(categoryFilter.toLowerCase()))) return false;

    return true;
  });

  const completedCount = filteredTasks.filter(t => t.completed).length;
  const pendingCount = filteredTasks.length - completedCount;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="text-center">
          <div className="relative w-10 h-10 mx-auto mb-3">
            <div className="absolute inset-0 rounded-full border-2" style={{ borderColor: '#e0e4e9' }}></div>
            <div className="absolute inset-0 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: '#7e1fff' }}></div>
          </div>
          <p className="text-sm" style={{ color: '#828a93' }}>Loading your tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f5f8fa' }}>
      {/* Yahoo-style Navigation */}
      <nav className="bg-white border-b" style={{ borderColor: '#e0e4e9', height: '57px' }}>
        <div className="max-w-7xl mx-auto px-4 h-full flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <button onClick={handleGoHome} className="text-xl font-semibold" style={{ color: '#7e1fff' }}>
              TaskFlow
            </button>
            <span className="text-xs" style={{ color: '#828a93' }}>/ Dashboard</span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleGoHome}
              className="text-sm px-3 py-2 rounded hover:bg-gray-50 hidden md:inline-flex"
              style={{ color: '#232a31' }}
            >
              Home
            </button>
            <button
              onClick={handleLogout}
              className="text-sm px-4 py-2 rounded"
              style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
            >
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="py-6 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          {/* Header Section - Yahoo Style */}
          <div className="mb-4">
            <h1 className="text-2xl font-semibold mb-1" style={{ color: '#232a31' }}>
              My Tasks
            </h1>
            <p className="text-sm" style={{ color: '#828a93' }}>
              {tasks.length} total · {completedCount} completed · {pendingCount} pending
            </p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="mb-6 bg-red-500/10 backdrop-blur-sm border border-red-500/30 rounded-xl p-4 animate-scale-in">
              <div className="flex items-start">
                <svg className="h-5 w-5 text-red-500 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Tasks Section */}
          <div className="bg-white rounded p-4" style={{ border: '1px solid #e0e4e9' }}>
            {/* Search & Advanced Filters */}
            <div className="mb-4 space-y-3">
              {/* Search Bar */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleApplyFilters()}
                  placeholder="Search tasks..."
                  className="flex-1 px-3 py-2 rounded text-sm"
                  style={{ border: '1px solid #e0e4e9' }}
                />
                <button
                  onClick={handleApplyFilters}
                  className="px-4 py-2 rounded text-sm font-medium"
                  style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
                >
                  Search
                </button>
              </div>

              {/* Filters Row */}
              <div className="flex gap-2 flex-wrap items-center">
                <select
                  value={priorityFilter}
                  onChange={(e) => setPriorityFilter(e.target.value as any)}
                  className="px-3 py-1.5 rounded text-xs"
                  style={{ border: '1px solid #e0e4e9' }}
                >
                  <option value="all">All Priorities</option>
                  <option value="high">🔴 High</option>
                  <option value="medium">🟡 Medium</option>
                  <option value="low">🟢 Low</option>
                </select>

                <input
                  type="text"
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  placeholder="Category..."
                  className="px-3 py-1.5 rounded text-xs w-32"
                  style={{ border: '1px solid #e0e4e9' }}
                />

                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-3 py-1.5 rounded text-xs"
                  style={{ border: '1px solid #e0e4e9' }}
                >
                  <option value="created_at">Created Date</option>
                  <option value="due_date">Due Date</option>
                  <option value="priority">Priority</option>
                  <option value="title">Title</option>
                </select>

                <button
                  onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                  className="px-2 py-1.5 rounded text-xs"
                  style={{ border: '1px solid #e0e4e9', color: '#6e7780' }}
                >
                  {sortOrder === 'asc' ? '↑' : '↓'}
                </button>

                <button
                  onClick={() => {
                    setSearchTerm('');
                    setPriorityFilter('all');
                    setCategoryFilter('');
                    setSortBy('created_at');
                    setSortOrder('desc');
                    loadTasks();
                  }}
                  className="px-3 py-1.5 rounded text-xs"
                  style={{ color: '#6e7780' }}
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Status Filter Tabs */}
            <div className="flex justify-between items-center mb-4 pb-3 border-b" style={{ borderColor: '#e0e4e9' }}>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setFilter('all')}
                  className="text-xs px-3 py-1.5 rounded font-medium"
                  style={filter === 'all' ? { backgroundColor: '#7e1fff', color: '#ffffff' } : { color: '#6e7780' }}
                >
                  All ({tasks.length})
                </button>
                <button
                  onClick={() => setFilter('pending')}
                  className="text-xs px-3 py-1.5 rounded font-medium"
                  style={filter === 'pending' ? { backgroundColor: '#7e1fff', color: '#ffffff' } : { color: '#6e7780' }}
                >
                  Pending ({pendingCount})
                </button>
                <button
                  onClick={() => setFilter('completed')}
                  className="text-xs px-3 py-1.5 rounded font-medium"
                  style={filter === 'completed' ? { backgroundColor: '#7e1fff', color: '#ffffff' } : { color: '#6e7780' }}
                >
                  Done ({completedCount})
                </button>
              </div>

              {/* Add Task Button */}
              <button
                onClick={handleCreateTask}
                className="text-sm px-4 py-2 rounded font-medium"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
              >
                + Add Task
              </button>
            </div>

            {/* Task Form or List */}
            {showForm ? (
              <div className="animate-scale-in">
                <TaskForm
                  task={editingTask || undefined}
                  onSuccess={handleFormSubmit}
                  onCancel={handleFormCancel}
                />
              </div>
            ) : (
              <div>
                {filteredTasks.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-sm mb-4" style={{ color: '#828a93' }}>
                      {filter === 'all' && 'No tasks yet'}
                      {filter === 'pending' && 'No pending tasks'}
                      {filter === 'completed' && 'No completed tasks'}
                    </p>
                    {filter === 'all' && (
                      <button
                        onClick={handleCreateTask}
                        className="text-sm px-4 py-2 rounded font-medium"
                        style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
                      >
                        Create Your First Task
                      </button>
                    )}
                  </div>
                ) : (
                  <TaskList
                    tasks={filteredTasks}
                    onTaskUpdate={handleTaskUpdate}
                    onTaskDelete={handleTaskDelete}
                    onTaskEdit={handleEditTask}
                  />
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskDashboardPage;
