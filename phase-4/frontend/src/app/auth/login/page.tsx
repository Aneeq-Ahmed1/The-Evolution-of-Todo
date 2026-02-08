"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const result = await signIn.email({
        email,
        password,
        callbackURL: "/dashboard",
      });

      if (result?.error) {
        setError(result.error.message || "Login failed. Please check your credentials.");
        setIsLoading(false);
      } else {
        router.push("/dashboard");
        router.refresh();
      }
    } catch (err) {
      setError("An error occurred during login. Please try again.");
      setIsLoading(false);
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4" style={{ backgroundColor: '#f5f8fa' }}>
      <div className="max-w-md w-full">
        {/* Back to Home Link */}
        <Link href="/" className="inline-flex items-center text-sm mb-4 hover:underline" style={{ color: '#6e7780' }}>
          ← Back to Home
        </Link>

        {/* Login Card - Yahoo Style */}
        <div className="bg-white rounded p-6" style={{ border: '1px solid #e0e4e9' }}>
          {/* Header */}
          <div className="mb-6">
            <h2 className="text-2xl font-semibold mb-1" style={{ color: '#232a31' }}>
              Sign In
            </h2>
            <p className="text-sm" style={{ color: '#6e7780' }}>
              Sign in to access your tasks
            </p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            {/* Error Alert */}
            {error && (
              <div className="p-3 rounded" style={{ backgroundColor: '#fee', border: '1px solid #fcc' }}>
                <p className="text-sm" style={{ color: '#c00' }}>{error}</p>
              </div>
            )}

            {/* Email Field */}
            <div>
              <label htmlFor="email-address" className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2.5 rounded text-sm"
                style={{
                  border: '1px solid #e0e4e9',
                  backgroundColor: '#ffffff',
                  color: '#232a31'
                }}
                placeholder="you@example.com"
                disabled={isLoading}
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2.5 rounded text-sm"
                style={{
                  border: '1px solid #e0e4e9',
                  backgroundColor: '#ffffff',
                  color: '#232a31'
                }}
                placeholder="Enter your password"
                disabled={isLoading}
              />
            </div>

            {/* Forgot Password Link */}
            <div className="text-right">
              <Link href="/auth/forgot-password" className="text-xs hover:underline" style={{ color: '#6e7780' }}>
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-2.5 rounded font-medium text-sm disabled:opacity-50"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
              >
                {isLoading ? 'Signing in...' : 'Sign In'}
              </button>
            </div>

            {/* Sign Up Link */}
            <div className="text-center pt-3 border-t" style={{ borderColor: '#e0e4e9' }}>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Don't have an account?{' '}
                <Link href="/auth/register" className="font-medium hover:underline" style={{ color: '#7e1fff' }}>
                  Sign up
                </Link>
              </p>
            </div>
          </form>
        </div>

        {/* Security Notice */}
        <div className="mt-4 text-center">
          <p className="text-xs" style={{ color: '#828a93' }}>
            Secured with JWT authentication
          </p>
        </div>
      </div>
    </div>
  );
}
