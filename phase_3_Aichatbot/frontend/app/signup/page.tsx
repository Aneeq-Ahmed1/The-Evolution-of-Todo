// frontend/app/signup/page.tsx
'use client';

import React, { useState } from 'react';
import SignupForm from '../../components/Auth/SignupForm';
import { useAuth } from '../../components/Auth/AuthProvider';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const SignupPage: React.FC = () => {
  const { signup, isAuthenticated } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  const handleSignup = async (credentials: { name: string; email: string; password: string; confirmPassword: string }) => {
    setIsLoading(true);
    setError(null);

    // Validate that passwords match
    if (credentials.password !== credentials.confirmPassword) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      await signup(credentials.name, credentials.email, credentials.password);
      // Redirect is handled by the AuthProvider
    } catch (err) {
      setError((err as Error).message || 'Signup failed. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-center text-gray-900">Todo App</h1>
          <p className="mt-2 text-center text-gray-600">Create your account</p>
        </div>
        <SignupForm onSignup={handleSignup} isLoading={isLoading} error={error ?? undefined} />

        <div className="text-center text-sm text-gray-600 mt-6">
          <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
            Already have an account? Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;