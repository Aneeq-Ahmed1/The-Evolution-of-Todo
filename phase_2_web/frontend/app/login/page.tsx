// frontend/app/login/page.tsx
'use client';

import React, { useState } from 'react';
import LoginForm from '../../components/Auth/LoginForm';
import { useAuth } from '../../components/Auth/AuthProvider';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const LoginPage: React.FC = () => {
  const { login, isAuthenticated } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  const handleLogin = async (credentials: { email: string; password: string }) => {
    setIsLoading(true);
    setError(null);

    try {
      await login(credentials.email, credentials.password);
      // Redirect is handled by the AuthProvider
    } catch (err) {
      setError((err as Error).message || 'Login failed. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-center text-gray-900">Todo App</h1>
          <p className="mt-2 text-center text-gray-600">Sign in to your account</p>
        </div>
        <LoginForm onLogin={handleLogin} isLoading={isLoading} error={error ?? undefined} />

        <div className="text-center text-sm text-gray-600 mt-6">
          <Link href="/signup" className="font-medium text-blue-600 hover:text-blue-500">
            Don't have an account? Sign up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;