'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f5f8fa' }}>
      {/* Yahoo-style Navigation */}
      <nav className="bg-white border-b" style={{ borderColor: '#e0e4e9', height: '57px' }}>
        <div className="max-w-7xl mx-auto px-4 h-full flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-semibold" style={{ color: '#7e1fff' }}>AI Task Assistant</h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => router.push('/chat')}
              className="text-sm px-4 py-2 rounded font-medium"
              style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
            >
              Open Chat
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section - Yahoo Style */}
      <section className="py-10 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <h1 className="text-3xl font-semibold mb-3" style={{ color: '#232a31' }}>
            AI-Powered Task Management
          </h1>
          <p className="text-base mb-6" style={{ color: '#6e7780' }}>
            Talk to your AI assistant to manage tasks naturally with simple conversation
          </p>

          <div className="flex gap-3 justify-center">
            <button
              onClick={() => router.push('/chat')}
              className="px-6 py-2.5 rounded font-medium text-sm"
              style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '44px' }}
            >
              Start Chatting with AI
            </button>
          </div>

          <div className="mt-4 flex justify-center gap-6 text-xs" style={{ color: '#828a93' }}>
            <span>✓ Natural Language</span>
            <span>✓ Smart Assistance</span>
            <span>✓ Secure & Private</span>
          </div>
        </div>
      </section>

      {/* Features - Yahoo Grid Style */}
      <section className="py-10" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-xl font-semibold text-center mb-6" style={{ color: '#232a31' }}>
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ Talk Naturally
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Simply tell the AI what you want to do using everyday language
              </p>
            </div>

            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ AI Processes
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Our smart AI understands your requests and manages your tasks
              </p>
            </div>

            <div className="bg-white p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
              <h3 className="text-sm font-semibold mb-1" style={{ color: '#232a31' }}>
                ✓ Tasks Organized
              </h3>
              <p className="text-sm" style={{ color: '#6e7780' }}>
                Your tasks are automatically created, updated, and tracked
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Example Commands */}
      <section className="py-8 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <h2 className="text-xl font-semibold mb-6" style={{ color: '#232a31' }}>
            Just Say Things Like...
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              "Add a task to buy groceries",
              "Show me my pending tasks",
              "Mark the report task as complete",
              "Delete my meeting task"
            ].map((command, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded" style={{ border: '1px solid #e0e4e9' }}>
                <p className="text-sm font-medium" style={{ color: '#232a31' }}>
                  "{command}"
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-8 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <p className="text-xs font-semibold mb-3" style={{ color: '#828a93' }}>
            POWERED BY
          </p>

          <div className="flex flex-wrap justify-center gap-3">
            {['Next.js', 'FastAPI', 'OpenAI', 'PostgreSQL', 'TypeScript'].map((tech) => (
              <span
                key={tech}
                className="px-3 py-1.5 rounded text-xs font-medium"
                style={{ backgroundColor: '#f0f3f5', color: '#232a31' }}
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-10" style={{ backgroundColor: '#f5f8fa' }}>
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-semibold mb-2" style={{ color: '#232a31' }}>
            Ready to Chat with Your AI Assistant?
          </h2>
          <p className="mb-6" style={{ color: '#6e7780' }}>
            Experience the future of task management with AI
          </p>
          <button
            onClick={() => router.push('/chat')}
            className="px-8 py-3 rounded font-medium text-sm"
            style={{ backgroundColor: '#7e1fff', color: '#ffffff', minHeight: '48px' }}
          >
            Start Chatting Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-6" style={{ backgroundColor: '#ffffff', borderColor: '#e0e4e9' }}>
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-xs mb-1" style={{ color: '#828a93' }}>
            <span className="font-semibold" style={{ color: '#7e1fff' }}>AI Task Assistant</span> - Intelligent Task Management
          </p>
          <p className="text-xs" style={{ color: '#828a93' }}>
            © 2026 AI Task Assistant. Powered by AI & Natural Language Processing
          </p>
        </div>
      </footer>
    </div>
  );
}
