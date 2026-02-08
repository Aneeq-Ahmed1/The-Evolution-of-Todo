'use client';

import { useRouter } from 'next/navigation';

export default function CTA() {
  const router = useRouter();

  const handleSignUp = () => {
    router.push('/auth/register');
  };

  return (
    <section className="py-20 bg-gradient-to-r from-indigo-600 to-purple-600" aria-labelledby="cta-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 id="cta-heading" className="text-3xl font-extrabold text-white sm:text-4xl">
            Ready to boost your productivity?
          </h2>
          <p className="mt-4 text-lg text-indigo-100">
            Join thousands of users who have transformed their task management experience with our cloud-native AI-powered todo application.
          </p>
          <div className="mt-10">
            <button
              onClick={handleSignUp}
              className="inline-flex items-center px-8 py-4 border border-transparent text-base font-medium rounded-md shadow-sm text-indigo-600 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white"
              aria-label="Get started with our todo application"
            >
              Get Started Today
            </button>
            <p className="mt-4 text-sm text-indigo-200">
              Free 14-day trial • No credit card required
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}