"use client";

import { useState } from "react";
import { signUp, signIn } from "@/lib/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match. Please make sure both passwords are identical.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    setIsLoading(true);

    try {
      const registerResult = await signUp.email({
        email,
        password,
      });

      if (registerResult?.error) {
        const errorMessage = registerResult.error.message || "Registration failed";

        if (errorMessage.includes("already registered") || errorMessage.includes("Email already registered")) {
          setError(`This email is already registered. Please use a different email or sign in instead.`);
        } else {
          setError(errorMessage);
        }
        setIsLoading(false);
        return;
      }

      const loginResult = await signIn.email({
        email,
        password,
        callbackURL: "/dashboard",
      });

      if (loginResult?.error) {
        setError("Registration successful! However, automatic login failed. Please sign in manually.");
        setIsLoading(false);
        setTimeout(() => router.push("/auth/login"), 2000);
      } else {
        router.push("/dashboard");
        router.refresh();
      }
    } catch (err) {
      setError("An unexpected error occurred during registration. Please try again.");
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

        {/* Register Card - Yahoo Style */}
        <div className="bg-white rounded p-6" style={{ border: '1px solid #e0e4e9' }}>
          {/* Header */}
          <div className="mb-6">
            <h2 className="text-2xl font-semibold mb-1" style={{ color: '#232a31' }}>
              Create Account
            </h2>
            <p className="text-sm" style={{ color: '#6e7780' }}>
              Join us and start managing your tasks
            </p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            {/* Error Alert */}
            {error && (
              <div className="p-3 rounded" style={{ backgroundColor: '#fee', border: '1px solid #fcc' }}>
                <p className="text-sm font-medium mb-1" style={{ color: '#c00' }}>Registration Error</p>
                <p className="text-sm" style={{ color: '#c00' }}>{error}</p>
                {error.includes("already registered") && (
                  <Link
                    href="/auth/login"
                    className="text-sm underline hover:no-underline mt-2 inline-block"
                    style={{ color: '#c00' }}
                  >
                    Go to Sign In →
                  </Link>
                )}
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
                autoComplete="new-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2.5 rounded text-sm"
                style={{
                  border: '1px solid #e0e4e9',
                  backgroundColor: '#ffffff',
                  color: '#232a31'
                }}
                placeholder="Create a password (min 6 characters)"
                disabled={isLoading}
              />
              <p className="mt-1 text-xs" style={{ color: '#828a93' }}>Must be at least 6 characters</p>
            </div>

            {/* Confirm Password Field */}
            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
                Confirm Password
              </label>
              <input
                id="confirm-password"
                name="confirm-password"
                type="password"
                autoComplete="new-password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-3 py-2.5 rounded text-sm"
                style={{
                  border: '1px solid #e0e4e9',
                  backgroundColor: '#ffffff',
                  color: '#232a31'
                }}
                placeholder="Confirm your password"
                disabled={isLoading}
              />
              {password && confirmPassword && password !== confirmPassword && (
                <p className="mt-1 text-xs" style={{ color: '#c00' }}>Passwords do not match</p>
              )}
              {password && confirmPassword && password === confirmPassword && (
                <p className="mt-1 text-xs" style={{ color: '#0a0' }}>✓ Passwords match</p>
              )}
            </div>

            {/* Submit Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-2.5 rounded font-medium text-sm disabled:opacity-50"
                style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
              >
                {isLoading ? 'Creating account...' : 'Create Account'}
              </button>
            </div>

            {/* Sign In Link */}
            <div className="text-center pt-3 border-t" style={{ borderColor: '#e0e4e9' }}>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Already have an account?{' '}
                <Link href="/auth/login" className="font-medium hover:underline" style={{ color: '#7e1fff' }}>
                  Sign in
                </Link>
              </p>
            </div>
          </form>
        </div>

        {/* Privacy Notice */}
        <div className="mt-4 text-center">
          <p className="text-xs" style={{ color: '#828a93' }}>
            By creating an account, you agree to our Terms & Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
}
