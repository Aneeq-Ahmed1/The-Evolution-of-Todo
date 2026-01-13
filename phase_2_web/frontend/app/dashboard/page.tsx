// frontend/app/dashboard/page.tsx
'use client';

import React from 'react';
import TodoList from '../../components/TodoList/TodoList';
import ProtectedRoute from '../../components/Auth/ProtectedRoute';
import { useAuth } from '../../components/Auth/AuthProvider';

const DashboardPage: React.FC = () => {
  const { logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-lg font-medium text-gray-900">Todo App</h1>
            <nav className="flex space-x-4">
              <button
                onClick={handleLogout}
                className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition-colors"
              >
                Logout
              </button>
            </nav>
          </div>
        </header>

        <main className="py-6 sm:py-8">
          <TodoList />
        </main>

        <footer className="bg-white border-t mt-8 py-4">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
            <p>© {new Date().getFullYear()} Todo App. Stay organized and productive.</p>
          </div>
        </footer>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;