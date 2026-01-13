'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authService } from '../../services/api/authService';
import { useRouter, usePathname } from 'next/navigation';

interface AuthContextType {
  user: any | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Calculate isAuthenticated
  const isAuthenticated = !!user && !!token;

  // Load user from localStorage on initial load
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');

    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser));
        setToken(storedToken);
      } catch (e) {
        // Clear invalid data if parsing fails
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }

    setIsLoading(false);
  }, []);

  // Check authentication on route change
  useEffect(() => {
    if (!isLoading) {
      const requiresAuth = pathname === '/dashboard';
      const isPublicRoute = pathname === '/login' || pathname === '/signup';

      if (requiresAuth && !isAuthenticated) {
        router.push('/login');
      } else if ((isPublicRoute || pathname === '/') && isAuthenticated) {
        // Redirect authenticated users away from login/signup
        if (pathname === '/login' || pathname === '/signup' || pathname === '/') {
          router.push('/dashboard');
        }
      }
    }
  }, [pathname, user, token, isLoading, router]);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const result = await authService.login({ email, password });
      setUser(result.user);
      setToken(result.token);

      // Store in localStorage
      localStorage.setItem('user', JSON.stringify(result.user));
      localStorage.setItem('token', result.token);

      router.push('/dashboard');
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      const result = await authService.signup({ name, email, password });
      setUser(result.user);
      setToken(result.token);

      // Store in localStorage
      localStorage.setItem('user', JSON.stringify(result.user));
      localStorage.setItem('token', result.token);

      router.push('/dashboard');
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      setUser(null);
      setToken(null);

      // Clear localStorage
      const storedUser = localStorage.getItem('user');
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      localStorage.removeItem('users'); // Also clear users data

      // Use the user-specific todos key for clearing
      if (storedUser) {
        try {
          const userData = JSON.parse(storedUser);
          const userTodosKey = `todos_${userData.id}`;
          localStorage.removeItem(userTodosKey);
        } catch (e) {
          // If parsing fails, try to remove the default key
          localStorage.removeItem('todos_default');
        }
      } else {
        localStorage.removeItem('todos_default');
      }

      router.push('/login');
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    token,
    isAuthenticated,
    login,
    signup,
    logout,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};