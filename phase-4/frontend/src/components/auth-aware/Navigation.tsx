'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { getJwtToken, isAuthenticated, signOut } from '../../lib/auth';
import ThemeToggle from '../ThemeToggle';

type AuthStatus = 'checking' | 'authenticated' | 'unauthenticated';
type NavigateFunction = (path: string) => void;

interface NavigationProps {
  authStatus: AuthStatus;
  onNavigate: NavigateFunction;
}

export default function AuthAwareNavigation({ authStatus, onNavigate }: NavigationProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await signOut();
      onNavigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <svg className="w-8 h-8 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">TodoApp</span>
            </Link>
          </div>

          <div className="flex items-center">
            <div className="hidden md:flex md:items-center md:space-x-4 md:ml-4">
              <div className="flex items-center justify-center">
                <ThemeToggle />
              </div>
              {authStatus === 'checking' ? (
                <div className="text-sm text-gray-500">Checking...</div>
              ) : authStatus === 'unauthenticated' ? (
                <>
                  <Link
                    href="/auth/forgot-password"
                    className="text-sm font-medium text-gray-600 hover:text-gray-900"
                  >
                    Forgot Password?
                  </Link>
                  <Link
                    href="/auth/login"
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Log In
                  </Link>
                  <Link
                    href="/auth/register"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    Sign Up
                  </Link>
                </>
              ) : (
                <>
                  <button
                    onClick={() => onNavigate('/dashboard/tasks')}
                    className="inline-flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    Dashboard
                  </button>
                  <button
                    onClick={handleLogout}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Logout
                  </button>
                </>
              )}
            </div>

            <div className="-mr-2 flex items-center md:hidden">
              <div className="flex items-center justify-center mr-2">
                <ThemeToggle />
              </div>
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
              >
                <span className="sr-only">Open main menu</span>
                <svg
                  className={`${mobileMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                <svg
                  className={`${mobileMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu, toggle classes based on menu state */}
      <div className={`${mobileMenuOpen ? 'block' : 'hidden'} md:hidden`}>
        <div className="pt-4 pb-3">
          <div className="flex items-center px-4 justify-between">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-10 h-10" />
              </div>
              <div className="ml-3">
                <div className="text-base font-medium text-gray-800 dark:text-gray-200">
                  {authStatus === 'authenticated' ? 'User' : 'Guest'}
                </div>
                <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  {authStatus === 'authenticated' ? 'user@example.com' : 'Not logged in'}
                </div>
              </div>
            </div>
            <div className="flex items-center justify-center">
              <ThemeToggle />
            </div>
          </div>
          <div className="mt-3 space-y-1">
            {authStatus === 'unauthenticated' ? (
              <>
                <Link
                  href="/auth/login"
                  className="block px-4 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700 rounded-md"
                >
                  Sign In
                </Link>
                <Link
                  href="/auth/register"
                  className="block px-4 py-2 text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md"
                >
                  Sign Up
                </Link>
                <Link
                  href="/auth/forgot-password"
                  className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700 rounded-md"
                >
                  Forgot Password?
                </Link>
              </>
            ) : (
              <>
                <button
                  onClick={() => onNavigate('/dashboard/tasks')}
                  className="block w-full text-left px-4 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700 rounded-md"
                >
                  Dashboard
                </button>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-base font-medium text-white bg-red-600 hover:bg-red-700 rounded-md"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}