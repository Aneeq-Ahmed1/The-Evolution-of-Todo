"use client";

import { useState } from "react";

export default function TestPage() {
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const testBackend = async () => {
    setLoading(true);
    setResult("Testing...");

    try {
      const response = await fetch("http://localhost:8000/");
      const data = await response.json();
      setResult(`✓ Backend is running: ${JSON.stringify(data)}`);
    } catch (err: any) {
      setResult(`✗ Backend connection failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testToken = () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setResult(`✓ Token exists: ${token.substring(0, 30)}...`);
    } else {
      setResult(`✗ No token found in localStorage`);
    }
  };

  const testTasksEndpoint = async () => {
    setLoading(true);
    setResult("Testing tasks endpoint...");

    const token = localStorage.getItem('access_token');
    if (!token) {
      setResult("✗ No token found. Please login first.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/tasks", {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setResult(`✓ Tasks endpoint working: ${JSON.stringify(data)}`);
      } else {
        const error = await response.json();
        setResult(`✗ Tasks endpoint error [${response.status}]: ${JSON.stringify(error)}`);
      }
    } catch (err: any) {
      setResult(`✗ Request failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold mb-6">Debug Test Page</h1>

          <div className="space-y-4">
            <button
              onClick={testBackend}
              disabled={loading}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              Test Backend Connection
            </button>

            <button
              onClick={testToken}
              className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Check Token in LocalStorage
            </button>

            <button
              onClick={testTasksEndpoint}
              disabled={loading}
              className="w-full px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:bg-gray-400"
            >
              Test Tasks Endpoint (with Auth)
            </button>

            <div className="mt-6 p-4 bg-gray-100 rounded">
              <h3 className="font-bold mb-2">Result:</h3>
              <pre className="whitespace-pre-wrap text-sm">{result || "Click a button to test"}</pre>
            </div>

            <div className="mt-4 text-sm text-gray-600">
              <p><strong>Note:</strong> Make sure backend is running on http://localhost:8000</p>
              <p className="mt-2">
                <a href="/auth/login" className="text-blue-600 hover:underline">Go to Login</a>
                {" | "}
                <a href="/auth/register" className="text-blue-600 hover:underline">Go to Register</a>
                {" | "}
                <a href="/dashboard/tasks" className="text-blue-600 hover:underline">Go to Tasks</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
